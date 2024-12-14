#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip jq gnome-terminal xterm unzip curl

# Install Knockpy
if ! command -v knockpy &> /dev/null; then
    echo "Installing Knockpy..."
    git clone https://github.com/guelfoweb/knock.git
    cd knock || exit
    sudo python3 setup.py install
    cd ..
    rm -rf knock
else
    echo "Knockpy is already installed."
fi

# Install Subfinder
if ! command -v subfinder &> /dev/null; then
    echo "Installing Subfinder..."
    curl -LO https://github.com/projectdiscovery/subfinder/releases/download/v2.4.5/subfinder_2.4.5_linux_amd64.zip
    unzip subfinder_2.4.5_linux_amd64.zip
    sudo mv subfinder /usr/local/bin/
    rm subfinder_2.4.5_linux_amd64.zip
else
    echo "Subfinder is already installed."
fi

# Install Assetfinder
if ! command -v assetfinder &> /dev/null; then
    echo "Installing Assetfinder..."
    go install github.com/tomnomnom/assetfinder@latest
    sudo mv ~/go/bin/assetfinder /usr/local/bin/
else
    echo "Assetfinder is already installed."
fi

# Install Subzy
if ! command -v subzy &> /dev/null; then
    echo "Installing Subzy..."
    go install github.com/LukaSikic/subzy@latest
    sudo mv ~/go/bin/subzy /usr/local/bin/
else
    echo "Subzy is already installed."
fi

# Install Httpx
if ! command -v httpx &> /dev/null; then
    echo "Installing Httpx..."
    go install github.com/projectdiscovery/httpx/cmd/httpx@latest
    sudo mv ~/go/bin/httpx /usr/local/bin/
else
    echo "Httpx is already installed."
fi

# Install Katana
if ! command -v katana &> /dev/null; then
    echo "Installing Katana..."
    go install github.com/projectdiscovery/katana/cmd/katana@latest
    sudo mv ~/go/bin/katana /usr/local/bin/
else
    echo "Katana is already installed."
fi

# Clean up
sudo apt autoremove -y

echo "Setup completed successfully."
