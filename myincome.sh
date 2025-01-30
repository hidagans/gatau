#!/bin/bash

# Error handling
set -e  # Exit on error
set -u  # Exit on undefined variable

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root"
  exit 1
fi

# Update system first
echo "Updating system..."
DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

# Install required packages
echo "Installing required packages..."
PACKAGES="wget sudo git unzip curl"
DEBIAN_FRONTEND=noninteractive apt-get install -y $PACKAGES

# Setup swap with error checking
echo "Setting up swap..."
if [ ! -f /swapfile ]; then
    sudo fallocate -l 4G /swapfile || dd if=/dev/zero of=/swapfile bs=1G count=4
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "Swap setup completed"
else
    echo "Swap file already exists"
fi

# Setup SSH with better security
echo "Setting up SSH..."
SSH_DIR=~/.ssh
if [ ! -d "$SSH_DIR" ]; then
    mkdir -p $SSH_DIR
    chmod 700 $SSH_DIR
fi

# Backup existing authorized_keys
if [ -f "$SSH_DIR/authorized_keys" ]; then
    cp $SSH_DIR/authorized_keys $SSH_DIR/authorized_keys.bak
fi

# Add SSH key
SSH_KEY='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCBWtUzXJs5bsSp2xfoRcVbXca2yAQLrISQ1dC5QF6zB+ys542auoWMCeqFPyfHYIxk/sWfyEk4AcdPBNeCu3PXXvM2dtNBCWNUFLs7TUYlNoHA4xjCmRYg0qQXal/7RZ3E8ALObBrcdJQjfFlUUKoDDdPz1+eRX/l4ra2ZX4CKromnMUv9xcOwCOXPjq6LAIbUoTwMWMBgpCTrHhvFKBkSY/zw2egStoncSvK1dbrf/wEZcoNM0xKZyiANCpRVaJ2y+XF9DEJNupQsc41pI9JtRmMeaejO7jfZFb8pMUoyBsDIS+u+4X3dF7BiLX+TCpacEQTsa/7/Xui1NSBCKK5H rsa-key-20241011'
echo "$SSH_KEY" >> $SSH_DIR/authorized_keys
chmod 600 $SSH_DIR/authorized_keys

# Clone repository with error handling
echo "Cloning repository..."
REPO_DIR="gege"
if [ -d "$REPO_DIR" ]; then
    echo "Removing existing repository..."
    rm -rf $REPO_DIR
fi

git clone https://github.com/hidagans/gege || {
    echo "Failed to clone repository"
    exit 1
}

# Run the scripts
cd $REPO_DIR || exit 1
echo "Installing Internet Income..."
DEBIAN_FRONTEND=noninteractive bash anu.sh --install

echo "Setup completed successfully!"
