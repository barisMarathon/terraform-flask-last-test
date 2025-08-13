import os
from flask import Flask, render_template, request
from ai import process_prompt, process_restaurant_json
from gpt_vision import process_image_prompt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Remove Terraform-related constants since they won't work in Azure App Service
# TERRAFORM_DIR = r"D:/terraform-sdx-project"
# SCRIPT_PATH = os.path.join(TERRAFORM_DIR, "install_flask_app.sh")

import os
import json
from flask import Flask, render_template, request
from ai import process_prompt, process_restaurant_json
from gpt_vision import process_image_prompt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

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
        
        # Handle GitHub URL (Note: Direct deployment removed for Azure App Service)
        github_url = request.form.get("github_url")
        if github_url:
            message = "Note: Direct deployment is not available in Azure App Service. The generated content is available through GitHub links provided by the AI services."

    return render_template("index.html", vm_ip=vm_ip, message=message, 
                         ai_response=ai_response, gpt_vision_response=gpt_vision_response)


@app.route("/destroy", methods=["POST"])
def destroy():
    message = "Resource management is not available in Azure App Service."
    return render_template("index.html", vm_ip=None, message=message)


if __name__ == "__main__":
    # For Azure App Service, use the PORT environment variable
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
