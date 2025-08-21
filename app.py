import os
import json
import subprocess
import tempfile
from flask import Flask, render_template, request
from ai import process_prompt, process_restaurant_json
from gpt_vision import process_image_prompt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

def deploy_github_url_to_vm(github_url):
    """
    Deploy GitHub URL to Azure VM using Terraform
    """
    try:
        # Update the install script with the new GitHub URL
        update_install_script(github_url)
        
        # Change to terraform directory
        terraform_dir = os.path.join(os.path.dirname(__file__), 'terraform')
        os.chdir(terraform_dir)
        
        # Initialize Terraform
        init_result = subprocess.run(['terraform', 'init'], 
                                   capture_output=True, text=True, check=True)
        print(f"Terraform init: {init_result.stdout}")
        
        # Apply Terraform configuration
        apply_result = subprocess.run(['terraform', 'apply', '-auto-approve'], 
                                    capture_output=True, text=True, check=True)
        print(f"Terraform apply: {apply_result.stdout}")
        
        # Get the public IP from Terraform output
        output_result = subprocess.run(['terraform', 'output', '-raw', 'public_ip'], 
                                     capture_output=True, text=True, check=True)
        public_ip = output_result.stdout.strip()
        
        print(f"VM deployed successfully with IP: {public_ip}")
        return public_ip
        
    except subprocess.CalledProcessError as e:
        print(f"Terraform command failed: {e.stderr}")
        return None
    except Exception as e:
        print(f"Deployment error: {e}")
        return None

def update_install_script(github_url):
    """
    Update the install_flask_app.sh script with the new GitHub URL
    """
    try:
        # Determine the raw GitHub URL format
        if 'github.com' in github_url:
            if '/blob/' in github_url:
                # Individual file URL - convert to raw format
                raw_url = github_url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
            else:
                # Repository URL - assume index.html in root
                if github_url.endswith('.git'):
                    github_url = github_url[:-4]  # Remove .git extension
                if not github_url.endswith('/'):
                    github_url += '/'
                raw_url = github_url.replace('github.com', 'raw.githubusercontent.com') + 'main/index.html'
        else:
            # Assume it's already a raw URL
            raw_url = github_url
        
        # Create new install script content
        script_content = f'''#!/bin/bash
sudo apt update
sudo apt install -y apache2 wget
sudo rm -rf /var/www/html/*

# Download the HTML file from GitHub
sudo wget -O /var/www/html/index.html "{raw_url}"

# Check if download was successful
if [ -f "/var/www/html/index.html" ]; then
    echo "Successfully downloaded HTML file from {raw_url}"
    sudo chmod -R 755 /var/www/html
    sudo systemctl restart apache2
else
    echo "Failed to download HTML file from {raw_url}"
    sudo echo "<html><body><h1>Error: Failed to download HTML file from {raw_url}</h1></body></html>" > /var/www/html/index.html
    sudo chmod -R 755 /var/www/html
    sudo systemctl restart apache2
fi

# Verify deployment
sudo ls -la /var/www/html/
'''
        
        # Write the updated script
        script_path = os.path.join(os.path.dirname(__file__), 'terraform', 'install_flask_app.sh')
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        print(f"Updated install script with URL: {raw_url}")
        
    except Exception as e:
        print(f"Error updating install script: {e}")
        raise

@app.route("/", methods=["GET", "POST"])
def index():
    vm_ip = None
    message = None
    ai_response = None
    gpt_vision_response = None

    if request.method == "POST":
        # Handle AI prompt (Claude)
        ai_prompt = request.form.get("ai_prompt")
        if ai_prompt:
            ai_response = process_prompt(ai_prompt)
        
        # Handle GPT Vision image upload
        uploaded_file = request.files.get("image_file")
        image_prompt = request.form.get("image_prompt", "")
        
        if uploaded_file and uploaded_file.filename != '':
            # Check if the file is an image
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
            file_extension = uploaded_file.filename.rsplit('.', 1)[1].lower()
            
            if file_extension in allowed_extensions:
                # Step 1: GPT Vision extracts restaurant data as JSON
                restaurant_json = process_image_prompt(uploaded_file, image_prompt)
                
                # Step 2: Claude generates website from JSON
                try:
                    # Try to parse as JSON to validate
                    # Clean the JSON string first to handle any extra whitespace or formatting
                    cleaned_json = restaurant_json.strip()
                    if cleaned_json.startswith('```json'):
                        # Remove markdown code block formatting if present
                        cleaned_json = cleaned_json.replace('```json', '').replace('```', '').strip()
                    
                    json.loads(cleaned_json)
                    # If JSON is valid, send it to Claude to generate the website
                    gpt_vision_response = process_restaurant_json(cleaned_json)
                except (json.JSONDecodeError, Exception) as e:
                    print(f"JSON parsing error: {e}")
                    print(f"Raw response: {restaurant_json[:200]}...")
                    # If JSON parsing fails, try to send the raw response to Claude anyway
                    # Sometimes GPT Vision returns valid restaurant data but not in perfect JSON format
                    gpt_vision_response = process_restaurant_json(restaurant_json)
            else:
                gpt_vision_response = "Error: Please upload a valid image file (PNG, JPG, JPEG, GIF, BMP, WebP)"
        
        # Handle GitHub URL - Deploy to Azure VM using Terraform
        github_url = request.form.get("github_url")
        if github_url:
            try:
                # Deploy to Azure VM using Terraform
                vm_ip = deploy_github_url_to_vm(github_url)
                if vm_ip:
                    message = f"Successfully deployed! Your site is live at: {vm_ip}"
                else:
                    message = "Deployment failed. Please check the logs."
            except Exception as e:
                print(f"Deployment error: {e}")
                message = f"Deployment failed: {str(e)}"

    return render_template("index.html", vm_ip=vm_ip, message=message, 
                         ai_response=ai_response, gpt_vision_response=gpt_vision_response)


@app.route("/destroy", methods=["POST"])
def destroy():
    """
    Destroy the Azure VM using Terraform
    """
    try:
        # Change to terraform directory
        terraform_dir = os.path.join(os.path.dirname(__file__), 'terraform')
        os.chdir(terraform_dir)
        
        # Destroy Terraform resources
        destroy_result = subprocess.run(['terraform', 'destroy', '-auto-approve'], 
                                      capture_output=True, text=True, check=True)
        print(f"Terraform destroy: {destroy_result.stdout}")
        
        message = "VM destroyed successfully!"
        
    except subprocess.CalledProcessError as e:
        print(f"Terraform destroy failed: {e.stderr}")
        message = f"Failed to destroy VM: {e.stderr}"
    except Exception as e:
        print(f"Destroy error: {e}")
        message = f"Error destroying VM: {str(e)}"
    
    return render_template("index.html", vm_ip=None, message=message)


if __name__ == "__main__":
    # For Azure App Service, use the PORT environment variable
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0", port=port, debug=False)