#!/bin/bash
set -e

echo "=== Environment Variables Debug ==="
echo "ARM_CLIENT_ID: ${ARM_CLIENT_ID:0:10}..."
echo "ARM_TENANT_ID: ${ARM_TENANT_ID:0:10}..."
echo "ARM_SUBSCRIPTION_ID: ${ARM_SUBSCRIPTION_ID:0:10}..."
echo "ARM_CLIENT_SECRET: ${ARM_CLIENT_SECRET:+[SET]}${ARM_CLIENT_SECRET:-[NOT SET]}"

# Export SP credentials for Terraform
export TF_VAR_client_id=$ARM_CLIENT_ID
export TF_VAR_client_secret=$ARM_CLIENT_SECRET
export TF_VAR_tenant_id=$ARM_TENANT_ID
export TF_VAR_subscription_id=$ARM_SUBSCRIPTION_ID
export TF_VAR_my_sub_id=$ARM_SUBSCRIPTION_ID

# Also set ARM_ variables for azurerm provider (this is the key fix)
export ARM_CLIENT_ID=$ARM_CLIENT_ID
export ARM_CLIENT_SECRET=$ARM_CLIENT_SECRET
export ARM_TENANT_ID=$ARM_TENANT_ID
export ARM_SUBSCRIPTION_ID=$ARM_SUBSCRIPTION_ID
export ARM_USE_CLI=false

echo "=== Terraform Variables Debug ==="
echo "TF_VAR_client_id: ${TF_VAR_client_id:0:10}..."
echo "ARM_CLIENT_ID: ${ARM_CLIENT_ID:0:10}..."
echo "ARM_USE_CLI: $ARM_USE_CLI"

# Generate SSH key if it doesn't exist in terraform directory
if [ ! -f /app/terraform/ssh_key ]; then
    ssh-keygen -t rsa -b 2048 -f /app/terraform/ssh_key -N ""
fi

# Set SSH public key path for Terraform
export TF_VAR_ssh_public_key_path="/app/terraform/ssh_key.pub"

cd /app/terraform
# terraform init
# terraform apply -auto-approve

# Start Flask app
exec python /app/app.py
