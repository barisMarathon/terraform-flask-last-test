import anthropic
import os
import datetime
import base64
from github import Github

def process_prompt(prompt):
    """
    Process the AI prompt using Claude API
    """
    try:
        # Get API key from environment variable
        api_key = os.getenv('ANTHROPIC_API_KEY')
        
        if not api_key:
            return "Error: ANTHROPIC_API_KEY environment variable not set"
        
        # Initialize the Anthropic client
        client = anthropic.Anthropic(api_key=api_key)
        
        # Send the prompt to Claude
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=7000,  # Increased token code generation stops if response is too long
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": """you need to generate *** ONLY *** 1 html page dont expalin anything else just generate the single webpage code and nothing else
                    here are the details of the html page: """ + prompt
                }
            ]
        )
        
        # Extract and return the response
        response = message.content[0].text
        print(f"Received prompt: {prompt}")
        print(f"Claude response: {response}")
        
        # Push the response to GitHub repository
        return push_to_github_from_prompt(response)
        
    except Exception as e:
        print(f"Error processing prompt: {e}")
        return f"Error: {str(e)}"

def process_restaurant_json(restaurant_json):
    """
    Process restaurant JSON data using Claude API to generate HTML website
    """
    try:
        # Get API key from environment variable
        api_key = os.getenv('ANTHROPIC_API_KEY')
        
        if not api_key:
            return "Error: ANTHROPIC_API_KEY environment variable not set"
        
        # Initialize the Anthropic client
        client = anthropic.Anthropic(api_key=api_key)
        
        # Clean the JSON string in case it has extra formatting
        cleaned_json = restaurant_json.strip()
        if cleaned_json.startswith('```json'):
            cleaned_json = cleaned_json.replace('```json', '').replace('```', '').strip()
        
        # Create a detailed prompt for restaurant website generation
        prompt = f"""You are an expert web developer. Generate a complete, modern, responsive HTML page for a restaurant menu using the provided data.

Requirements:
* Output ONLY valid HTML code (no explanations or markdown)
* Use internal <style> tags for all CSS
* Create stunning, modern design with premium feel
* Fully responsive (mobile, tablet, desktop)
* Include smooth animations and hover effects
* Parse and display all menu data dynamically

Design Focus:
* Modern glass-morphism or gradient backgrounds
* Premium typography combinations
* Interactive hover effects and micro-animations
* Professional color schemes (dark with accents or vibrant gradients)
* Card-based layouts with proper spacing
* Mobile-first responsive grid systems

Technical:
* Use CSS Grid/Flexbox for layouts
* CSS custom properties for theming
* Smooth transitions and transforms
* Backdrop filters for glass effects
* No external dependencies

Here is the restaurant data (might be JSON or structured text):
{cleaned_json}

Parse this data and create a beautiful restaurant website that displays the restaurant name, menu items, and prices in an attractive layout."""
        
        # Send the prompt to Claude
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract and return the response
        html_response = message.content[0].text
        print(f"Claude generated restaurant website from JSON")
        print(f"HTML length: {len(html_response)} characters")
        
        # Push the response to GitHub repository
        return push_to_github_from_json(html_response)
        
    except Exception as e:
        print(f"Error processing restaurant JSON: {e}")
        return f"Error: {str(e)}"

def push_to_github_from_prompt(html_content):
    """
    Push HTML content to GitHub from text prompt
    """
    try:
        # Get GitHub token from environment variable
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            return "Error: GITHUB_TOKEN environment variable not set. Please set your GitHub Personal Access Token."
        
        print(f"Using GitHub token: {github_token[:8]}...")  # Show first 8 chars for debugging
        
        # Initialize GitHub client
        g = Github(github_token)
        
        # Test authentication first
        user = g.get_user()
        print(f"Authenticated as: {user.login}")
        
        # Get the repository
        repo_name = "barisMarathon/html-pages-storage"
        repo = g.get_repo(repo_name)
        print(f"Repository found: {repo.full_name}, Private: {repo.private}")
        
        # Create a filename based on timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_page_{timestamp}.html"
        
        # Create or update the file in the repository
        try:
            # Try to get existing file (will fail if it doesn't exist)
            existing_file = repo.get_contents(filename)
            # If file exists, update it
            repo.update_file(
                path=filename,
                message=f"Update generated HTML page - {timestamp}",
                content=html_content,
                sha=existing_file.sha
            )
            action = "updated"
        except:
            # File doesn't exist, create new one
            repo.create_file(
                path=filename,
                message=f"Add generated HTML page - {timestamp}",
                content=html_content
            )
            action = "created"
        
        repo_url = f"https://github.com/{repo_name}/blob/main/{filename}"
        return f"HTML page {action} successfully! View at: {repo_url}"
        
    except Exception as github_error:
        print(f"Error pushing to GitHub: {github_error}")
        print(f"Error type: {type(github_error)}")
        return f"AI response generated but failed to push to GitHub: {str(github_error)}"

def push_to_github_from_json(html_content):
    """
    Push HTML content to GitHub from restaurant JSON
    """
    try:
        # Get GitHub token from environment variable
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            return "Error: GITHUB_TOKEN environment variable not set"
        
        # Initialize GitHub client
        g = Github(github_token)
        
        # Get the repository
        repo_name = "barisMarathon/html-pages-storage"
        repo = g.get_repo(repo_name)
        
        # Create a filename based on timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"restaurant_website_{timestamp}.html"
        
        # Create the file in the repository
        repo.create_file(
            path=filename,
            message=f"Add restaurant website generated from JSON - {timestamp}",
            content=html_content
        )
        
        repo_url = f"https://github.com/{repo_name}/blob/main/{filename}"
        return f"Restaurant website created successfully from image data! View at: {repo_url}"
        
    except Exception as github_error:
        print(f"Error pushing to GitHub: {github_error}")
        return f"HTML generated from JSON but failed to push to GitHub: {str(github_error)}"