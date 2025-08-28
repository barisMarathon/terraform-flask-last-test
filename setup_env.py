#lokal test için gerekli normalde gerek yok 
"""
Helper script to set up environment variables for the Flask app
Run this before starting your Flask application
"""
import os

def setup_environment():
    """
    Set up environment variables for the application
    """
    # Setup Anthropic API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("ANTHROPIC_API_KEY environment variable not found.")
        print("Please get your API key from: https://console.anthropic.com/")
        api_key = input("Enter your Anthropic API key: ").strip()
        
        if api_key:
            os.environ['ANTHROPIC_API_KEY'] = api_key
            print("✅ Anthropic API key set successfully!")
        else:
            print("❌ No Anthropic API key provided")
    else:
        print("✅ ANTHROPIC_API_KEY is already set")
    
    # Setup OpenAI API key
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        print("\nOPENAI_API_KEY environment variable not found.")
        print("Please get your API key from: https://platform.openai.com/api-keys")
        openai_key = input("Enter your OpenAI API key: ").strip()
        
        if openai_key:
            os.environ['OPENAI_API_KEY'] = openai_key
            print("✅ OpenAI API key set successfully!")
        else:
            print("❌ No OpenAI API key provided")
    else:
        print("✅ OPENAI_API_KEY is already set")
    
    # Setup GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("\nGITHUB_TOKEN environment variable not found.")
        print("Please get your Personal Access Token from: https://github.com/settings/tokens")
        print("Make sure to give it 'repo' permissions")
        github_token = input("Enter your GitHub Personal Access Token: ").strip()
        
        if github_token:
            os.environ['GITHUB_TOKEN'] = github_token
            print("✅ GitHub token set successfully!")
        else:
            print("❌ No GitHub token provided")
    else:
        print("✅ GITHUB_TOKEN is already set")
    
    # Show instructions for permanent setup
    if api_key or openai_key or github_token:
        print("\n📝 To make these permanent, add them to your system environment or create a .env file:")
        if api_key:
            print(f"ANTHROPIC_API_KEY={api_key}")
        if openai_key:
            print(f"OPENAI_API_KEY={openai_key}")
        if github_token:
            print(f"GITHUB_TOKEN={github_token}")
    
    return bool(api_key and openai_key and github_token)

if __name__ == "__main__":
    setup_environment()
