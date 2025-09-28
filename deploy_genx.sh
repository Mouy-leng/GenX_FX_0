#!/bin/bash

# GenX_FX Deployment Script for Google VM
# Run this script on your VM to deploy the backend

set -e

echo "🚀 Starting GenX_FX Deployment..."

# Update system and install dependencies
echo "📦 Installing dependencies..."
sudo apt update
sudo apt install -y docker.io docker-compose curl wget git nginx certbot python3-certbot-nginx

# Start and enable Docker
echo "🐳 Setting up Docker..."
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

# Create project directory
echo "📁 Setting up project directory..."
mkdir -p ~/GenX_FX
cd ~/GenX_FX

# Create .env.example file and prompt user for input
echo "🔧 Creating .env.example file..."
cat > .env.example << 'EOF'
# === Docker Registry Credentials ===
DOCKER_USERNAME=your_docker_username
DOCKER_PASSWORD=your_docker_password
DOCKER_IMAGE=your_docker_image
DOCKER_TAG=latest

# === API Keys ===
GEMINI_API_KEY=your_gemini_api_key
VANTAGE_ALPHAVANTAGE_API_KEY=your_alphavantage_api_key
NEWS_API_KEY=your_news_api_key
NEWSDATA_API_KEY=your_newsdata_api_key
FINNHUB_API_KEY=your_finnhub_api_key

# === Telegram Credentials ===
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_USER_ID=your_telegram_user_id

# === Gmail Credentials ===
GMAIL_USER=your_gmail_user
GMAIL_PASSWORD=your_gmail_password
GMAIL_APP_API_KEY=your_gmail_app_api_key

# === Reddit Credentials ===
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=GenX-Trading-Bot/1.0

# === FXCM Credentials ===
FXCM_USERNAME=your_fxcm_username
FXCM_PASSWORD=your_fxcm_password
FXCM_CONNECTION_TYPE=Demo
FXCM_URL=www.fxcorporate.com/Hosts.jsp

# === Security Keys ===
JWT_SECRET_KEY=your_jwt_secret_key

# === Feature Flags ===
ENABLE_NEWS_ANALYSIS=true
ENABLE_REDDIT_ANALYSIS=true
ENABLE_WEBSOCKET_FEED=true
API_PROVIDER=gemini
EOF

if [ ! -f .env ]; then
    echo "🛑 IMPORTANT: A '.env.example' file has been created."
    echo "Please copy it to '.env' and fill in your actual credentials."
    echo "    cp .env.example .env"
    echo "    nano .env"
    echo "The script will now exit. Please run it again after creating your .env file."
    exit 1
fi

# Clone the repository
echo "📥 Cloning GenX_FX repository..."
git clone https://github.com/Mouy-leng/GenX_FX.git temp_genx
cp -r temp_genx/* .
rm -rf temp_genx

# Create Docker Compose file for production with HTTPS
echo "🐳 Creating Docker Compose configuration..."
cat > docker-compose.production.yml << 'EOF'
version: '3.8'

services:
  genx-backend:
    build: .
    container_name: genx-backend
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
    env_file:
      - .env
    volumes:
      - ./expert-advisors:/app/expert-advisors
      - ./scripts:/app/scripts
      - ./logs:/app/logs
    networks:
      - genx-network

  nginx:
    image: nginx:alpine
    container_name: genx-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - genx-backend
    networks:
      - genx-network

networks:
  genx-network:
    driver: bridge

volumes:
  logs:
EOF

# Create Nginx configuration for HTTPS
echo "🌐 Creating Nginx configuration..."
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream genx_backend {
        server genx-backend:8080;
    }

    # HTTP to HTTPS redirect
    server {
        listen 80;
        server_name _;
        return 301 https://$host$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl;
        server_name _;

        # Self-signed certificate (replace with Let's Encrypt later)
        ssl_certificate /etc/nginx/ssl/nginx.crt;
        ssl_certificate_key /etc/nginx/ssl/nginx.key;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            proxy_pass http://genx_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /ws {
            proxy_pass http://genx_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }
    }
}
EOF

# Create SSL directory and generate self-signed certificate
echo "🔒 Setting up SSL certificate..."
mkdir -p ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/nginx.key -out ssl/nginx.crt \
    -subj "/C=US/ST=State/L=City/O=GenX/CN=localhost"

# Set proper permissions
chmod 600 ssl/nginx.key
chmod 644 ssl/nginx.crt

# Build and start the containers
echo "🏗️ Building and starting containers..."
sudo docker-compose -f docker-compose.production.yml up -d --build

# Wait for containers to start
echo "⏳ Waiting for containers to start..."
sleep 30

# Check container status
echo "📊 Container status:"
sudo docker ps

# Show logs
echo "📋 Recent logs:"
sudo docker-compose -f docker-compose.production.yml logs --tail=20

echo "✅ Deployment completed!"
echo "🌐 Your GenX_FX backend is now running on:"
echo "   - HTTP: http://$(curl -s ifconfig.me):80 (redirects to HTTPS)"
echo "   - HTTPS: https://$(curl -s ifconfig.me):443"
echo "   - Backend API: http://$(curl -s ifconfig.me):8080"

echo "📁 EA Scripts are available in: ~/GenX_FX/expert-advisors/"
echo "📁 Additional scripts in: ~/GenX_FX/scripts/"

echo "🔧 To view logs: sudo docker-compose -f docker-compose.production.yml logs -f"
echo "🔧 To stop: sudo docker-compose -f docker-compose.production.yml down"
echo "🔧 To restart: sudo docker-compose -f docker-compose.production.yml restart"