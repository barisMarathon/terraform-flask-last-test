#bu file a ihtiyaç yok

#!/usr/bin/env python3
"""
Azure App Service deployment helper script
"""
import os
import subprocess
import sys

def check_azure_cli():
    """Check if Azure CLI is installed"""
    try:
        subprocess.run(["az", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def deploy_to_azure():
    """Deploy the Flask app to Azure App Service"""
    
    if not check_azure_cli():
        print("❌ Azure CLI is not installed. Please install it first:")
        print("   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli")
        return False
    
    print("🚀 Starting Azure App Service deployment...")
    
    # Check if user is logged in to Azure
    try:
        subprocess.run(["az", "account", "show"], capture_output=True, check=True)
        print("✅ Azure authentication verified")
    except subprocess.CalledProcessError:
        print("❌ Please login to Azure first: az login")
        return False
    
    # Variables (you should customize these)
    APP_NAME = "menu-app-flask"  # This must be globally unique
    RESOURCE_GROUP = "menu-app-rg"
    LOCATION = "East US"
    
    print(f"📋 Configuration:")
    print(f"   App Name: {APP_NAME}")
    print(f"   Resource Group: {RESOURCE_GROUP}")
    print(f"   Location: {LOCATION}")
    
    try:
        # Create resource group
        print("🏗️  Creating resource group...")
        subprocess.run([
            "az", "group", "create",
            "--name", RESOURCE_GROUP,
            "--location", LOCATION
        ], check=True)
        
        # Create App Service plan
        print("📦 Creating App Service plan...")
        subprocess.run([
            "az", "appservice", "plan", "create",
            "--name", f"{APP_NAME}-plan",
            "--resource-group", RESOURCE_GROUP,
            "--sku", "B1",  # Basic tier
            "--is-linux"
        ], check=True)
        
        # Create Web App
        print("🌐 Creating Web App...")
        subprocess.run([
            "az", "webapp", "create",
            "--name", APP_NAME,
            "--resource-group", RESOURCE_GROUP,
            "--plan", f"{APP_NAME}-plan",
            "--runtime", "PYTHON:3.11"
        ], check=True)
        
        # Configure startup command
        print("⚙️  Configuring startup command...")
        subprocess.run([
            "az", "webapp", "config", "set",
            "--name", APP_NAME,
            "--resource-group", RESOURCE_GROUP,
            "--startup-file", "startup.sh"
        ], check=True)
        
        # Deploy code
        print("📤 Deploying code...")
        subprocess.run([
            "az", "webapp", "up",
            "--name", APP_NAME,
            "--resource-group", RESOURCE_GROUP,
            "--location", LOCATION,
            "--runtime", "PYTHON:3.11"
        ], check=True)
        
        print("\n🎉 Deployment completed!")
        print(f"🌍 Your app is available at: https://{APP_NAME}.azurewebsites.net")
        print("\n⚠️  Don't forget to set your environment variables:")
        print("   - ANTHROPIC_API_KEY")
        print("   - OPENAI_API_KEY") 
        print("   - GITHUB_TOKEN")
        print("\n🔧 You can set them using:")
        print(f"   az webapp config appsettings set --name {APP_NAME} --resource-group {RESOURCE_GROUP} --settings ANTHROPIC_API_KEY='your-key'")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "deploy":
        deploy_to_azure()
    else:
        print("Usage: python deploy.py deploy")
        print("This script will deploy your Flask app to Azure App Service")
