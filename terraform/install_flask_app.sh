#!/bin/bash
sudo apt update
sudo apt install -y apache2 wget
sudo rm -rf /var/www/html/*

# Download the HTML file directly
sudo wget -O /var/www/html/index.html "https://raw.githubusercontent.com/barisMarathon/html-pages-storage/main/restaurant_website_20250811_141232.html"

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
