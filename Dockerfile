# Step 1: Base image with Python 3.12
FROM python:3.12-slim

# Step 2: Install dependencies (Terraform + other tools + openssh-client + Azure CLI)
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    git \
    bash \
    openssh-client \
    ca-certificates \
    gnupg \
    lsb-release \
    && curl -sL https://aka.ms/InstallAzureCLIDeb | bash \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Install Terraform
RUN wget https://releases.hashicorp.com/terraform/1.12.1/terraform_1.12.1_linux_amd64.zip \
    -O /tmp/terraform.zip && \
    unzip /tmp/terraform.zip -d /usr/local/bin && \
    rm /tmp/terraform.zip

# Step 4: Generate SSH key pair
RUN mkdir -p ~/.ssh && \
    ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa -N "" && \
    chmod 600 ~/.ssh/id_rsa && \
    chmod 644 ~/.ssh/id_rsa.pub

# Step 5: Set workdir and copy your code
WORKDIR /app
COPY . /app

# Step 6: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt python-dotenv

# Step 7: Copy entrypoint script and make executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Step 8: Make terraform install script executable
RUN chmod +x /app/terraform/install_flask_app.sh

# Step 9: Expose Flask port
EXPOSE 80
ENV PORT=80

# Step 10: Use entrypoint to export TF vars & start Flask
ENTRYPOINT ["/entrypoint.sh"]