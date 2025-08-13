from flask import Flask, render_template, request
import subprocess
import os
import json
from ai import process_prompt, process_restaurant_json
from gpt_vision import process_image_prompt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

TERRAFORM_DIR = r"D:/terraform-sdx-project"
SCRIPT_PATH = os.path.join(TERRAFORM_DIR, "install_flask_app.sh")

@app.route("/", methods=["GET", "POST"])
def index():
    link = None
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
        
        # Handle GitHub URL deployment (enhanced to support both repos and individual HTML files)
        github_url = request.form.get("github_url")
        if github_url:
            # Check if it's an individual HTML file URL or a repository URL
            if "github.com" in github_url and "/blob/" in github_url and github_url.endswith('.html'):
                # Individual HTML file URL
                raw_url = github_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                
                # Create deployment script that downloads the HTML file directly
                with open(SCRIPT_PATH, "w") as f:
                    f.write(f"""#!/bin/bash
sudo apt update
sudo apt install -y apache2 wget
sudo rm -rf /var/www/html/*

# Download the HTML file directly
sudo wget -O /var/www/html/index.html "{raw_url}"

# Check if download was successful
if [ -f "/var/www/html/index.html" ]; then
    echo "Successfully downloaded HTML file"
    sudo chmod -R 755 /var/www/html
    sudo systemctl restart apache2
else
    echo "Failed to download HTML file"
    sudo echo "<html><body><h1>Error: Failed to download HTML file</h1></body></html>" > /var/www/html/index.html
    sudo chmod -R 755 /var/www/html
    sudo systemctl restart apache2
fi

# Verify deployment
sudo ls -la /var/www/html/
""")
                os.chmod(SCRIPT_PATH, 0o755)

                # Terraform komutlarını çalıştır
                try:
                    subprocess.run(["terraform", "init"], cwd=TERRAFORM_DIR, check=True)
                    subprocess.run(["terraform", "plan"], cwd=TERRAFORM_DIR, check=True)
                    subprocess.run(["terraform", "apply", "-auto-approve"], cwd=TERRAFORM_DIR, check=True)
                    vm_ip = subprocess.check_output(["terraform", "output", "-raw", "vm_public_ip"], cwd=TERRAFORM_DIR, text=True).strip()
                    vm_ip_with_protocol = f"http://{vm_ip}" if not vm_ip.startswith('http') else vm_ip
                    message = f"Successfully deployed HTML file! Access at: {vm_ip_with_protocol}"
                except subprocess.CalledProcessError as e:
                    message = f"Terraform komutlarında hata oluştu: {e}"
            else:
                # Traditional repository URL
                with open(SCRIPT_PATH, "w") as f:
                    f.write(f"""#!/bin/bash
sudo apt update
sudo apt install -y apache2 git
sudo rm -rf /var/www/html/*
sudo git clone {github_url} /var/www/html
sudo chmod -R 755 /var/www/html
sudo systemctl restart apache2
""")
                os.chmod(SCRIPT_PATH, 0o755)

                # Terraform komutlarını çalıştır
                try:
                    subprocess.run(["terraform", "init"], cwd=TERRAFORM_DIR, check=True)
                    subprocess.run(["terraform", "plan"], cwd=TERRAFORM_DIR, check=True)
                    subprocess.run(["terraform", "apply", "-auto-approve"], cwd=TERRAFORM_DIR, check=True)
                    vm_ip = subprocess.check_output(["terraform", "output", "-raw", "vm_public_ip"], cwd=TERRAFORM_DIR, text=True).strip()
                    vm_ip_with_protocol = f"http://{vm_ip}" if not vm_ip.startswith('http') else vm_ip
                    message = f"Successfully deployed repository! Access at: {vm_ip_with_protocol}"
                except subprocess.CalledProcessError as e:
                    message = f"Terraform komutlarında hata oluştu: {e}"

    return render_template("index.html", vm_ip=vm_ip, message=message, 
                         ai_response=ai_response, gpt_vision_response=gpt_vision_response)


@app.route("/destroy", methods=["POST"])
def destroy():
    message = None
    try:
        subprocess.run(["terraform", "destroy", "-auto-approve"], cwd=TERRAFORM_DIR, check=True)
        message = "Tüm kaynaklar başarıyla silindi."
    except subprocess.CalledProcessError as e:
        message = f"Destroy sırasında hata oluştu: {e}"

    return render_template("index.html", vm_ip=None, link=None, message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
