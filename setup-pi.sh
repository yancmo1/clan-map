#!/bin/bash

# Pi Server Setup Script for Clan Map
# This script sets up the clan-map application on Raspberry Pi with Cloudflare tunnel

set -e

echo "🏴‍☠️ Setting up Clan Map Server on Raspberry Pi..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker pi
    rm get-docker.sh
    echo "⚠️  Please log out and log back in for Docker permissions to take effect"
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo "🔧 Installing Docker Compose..."
    sudo pip3 install docker-compose
fi

# Navigate to project directory
cd /home/pi/clan-map

# Build and start the application
echo "🚀 Building and starting the Clan Map application..."
docker-compose down 2>/dev/null || true
docker-compose build
docker-compose up -d

# Wait for application to start
echo "⏳ Waiting for application to start..."
sleep 15

# Test the application
echo "🧪 Testing application..."
if curl -f http://localhost:5010/ > /dev/null 2>&1; then
    echo "✅ Application is running successfully on port 5010!"
else
    echo "❌ Application test failed"
    docker-compose logs
    exit 1
fi

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo "☁️  Installing Cloudflare tunnel..."
    
    # Download and install cloudflared for ARM64
    wget -O cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
    sudo dpkg -i cloudflared.deb
    rm cloudflared.deb
fi

# Create Cloudflare tunnel configuration
echo "🔧 Setting up Cloudflare tunnel configuration..."
mkdir -p ~/.cloudflared

# Create tunnel config
cat > ~/.cloudflared/config.yml << EOF
tunnel: clanmap
credentials-file: ~/.cloudflared/clanmap.json

ingress:
  - hostname: map.yancmo.xyz
    service: http://localhost:5010
  - service: http_status:404
EOF

echo "📋 Cloudflare tunnel configuration created."
echo "
🎯 Next steps to complete setup:

1. Authenticate with Cloudflare (if not done already):
   cloudflared tunnel login

2. Create the tunnel (if not done already):
   cloudflared tunnel create clanmap

3. Set up DNS routing:
   cloudflared tunnel route dns clanmap map.yancmo.xyz

4. Start the tunnel:
   cloudflared tunnel run clanmap

5. To run tunnel as a service:
   sudo cloudflared service install
   sudo systemctl start cloudflared
   sudo systemctl enable cloudflared

🚀 Your Clan Map application is now running on:
   - Local: http://localhost:5010
   - Public: https://map.yancmo.xyz (after tunnel setup)

📊 Useful commands:
   - Check app status: docker-compose ps
   - View app logs: docker-compose logs -f
   - Restart app: docker-compose restart
   - Stop app: docker-compose down
"
