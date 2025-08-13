"""
GPT Vision API operations for photo-based restaurant data extraction
"""
import os
import base64
from openai import OpenAI
from PIL import Image
import io

def encode_image_to_base64(image_file):
    """
    Convert uploaded image to base64 string
    """
    try:
        # Read the image file
        image = Image.open(image_file)
        
        # Convert to RGB if needed (for JPEG compatibility)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save to bytes buffer
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=85)
        
        # Encode to base64
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return img_base64
        
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

def process_image_prompt(image_file, custom_prompt=""):
    """
    Process image with GPT Vision API to generate HTML
    """
    try:
        # Get OpenAI API key from environment variable
        openai_api_key = os.getenv('OPENAI_API_KEY')
        
        if not openai_api_key:
            return "Error: OPENAI_API_KEY environment variable not set"
        
        # Initialize OpenAI client
        client = OpenAI(api_key=openai_api_key)
        
        # Encode image to base64
        base64_image = encode_image_to_base64(image_file)
        if not base64_image:
            return "Error: Failed to process the uploaded image"
        
        # Create the prompt for restaurant data extraction
        system_prompt = """You need to analyze the image and extract restaurant information. Return ONLY a JSON object with the following structure:

{
  "restaurant_name": "Name of the restaurant",
  "products": [
    {
      "name": "Product name",
      "price": "Price as string (e.g., '$12.99')",
      "description": "Brief description if available"
    }
  ]
}

Do not include any explanatory text, just return the JSON object."""
        
        user_prompt = f"Extract restaurant information from this image. Focus on menu items, prices, and restaurant name. {custom_prompt}" if custom_prompt else "Extract restaurant information from this image. Focus on menu items, prices, and restaurant name."
        
        # Send request to GPT-4 Vision
        response = client.chat.completions.create(
            model="gpt-4o",  # GPT-4 Omni has vision capabilities
            max_tokens=3000,
            temperature=0.7,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ]
        )
        
        # Extract the restaurant data JSON
        restaurant_data = response.choices[0].message.content
        print(f"GPT Vision extracted restaurant data")
        print(f"JSON data: {restaurant_data}")
        
        # Return the JSON data instead of pushing to GitHub
        return restaurant_data
        
    except Exception as e:
        error_message = str(e)
        print(f"GPT Vision Error: {error_message}")
        return f"Error: {error_message}"
