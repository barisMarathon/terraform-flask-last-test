# Menu App - Azure App Service Deployment

This Flask application provides AI-powered menu generation and image processing capabilities.

## Features

- AI text prompts for HTML generation (Claude)
- Image-to-menu extraction (GPT Vision)
- GitHub integration for storing generated content

## Azure App Service Deployment

### Prerequisites

1. Install Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
2. Login to Azure: `az login`
3. Have your API keys ready:
   - `ANTHROPIC_API_KEY` (for Claude AI)
   - `OPENAI_API_KEY` (for GPT Vision)
   - `GITHUB_TOKEN` (for GitHub integration)

### Quick Deployment

1. Run the deployment script:
   ```bash
   python deploy.py deploy
   ```

### Manual Deployment

1. Create a resource group:

   ```bash
   az group create --name menu-app-rg --location "East US"
   ```

2. Create an App Service plan:

   ```bash
   az appservice plan create --name menu-app-plan --resource-group menu-app-rg --sku B1 --is-linux
   ```

3. Create the web app:

   ```bash
   az webapp create --name YOUR-APP-NAME --resource-group menu-app-rg --plan menu-app-plan --runtime "PYTHON:3.11"
   ```

4. Deploy the code:
   ```bash
   az webapp up --name YOUR-APP-NAME --resource-group menu-app-rg --location "East US" --runtime "PYTHON:3.11"
   ```

### Environment Variables

Set your environment variables in Azure:

```bash
az webapp config appsettings set --name YOUR-APP-NAME --resource-group menu-app-rg --settings \
  ANTHROPIC_API_KEY="your-anthropic-key" \
  OPENAI_API_KEY="your-openai-key" \
  GITHUB_TOKEN="your-github-token"
```

### Local Development

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file with your API keys:

   ```
   ANTHROPIC_API_KEY=your-anthropic-key
   OPENAI_API_KEY=your-openai-key
   GITHUB_TOKEN=your-github-token
   ```

3. Run locally:
   ```bash
   python app.py
   ```

## Files Added for Azure Deployment

- `startup.sh` - Azure startup script
- `web.config` - IIS configuration for Windows App Service
- `.deployment` - Azure deployment configuration
- `runtime.txt` - Python version specification
- `azure-settings.json` - Azure application settings
- `deploy.py` - Automated deployment helper

## Important Notes

- Terraform functionality has been removed as it's not compatible with Azure App Service
- The app now only provides AI generation and GitHub integration
- Make sure your App Service name is globally unique
- Consider using Application Insights for monitoring
