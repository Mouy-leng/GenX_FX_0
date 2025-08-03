#!/bin/bash

# Comprehensive Railway Deployment Script for GenX FX Trading System
# This script provides multiple deployment options

set -e

RAILWAY_TOKEN="b82dcb0b-b5da-41ba-9541-7aac3471eb96"
PROJECT_NAME="genx-fx-trading"

echo "🚀 GenX FX Trading System - Railway Deployment"
echo "=============================================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Railway CLI
install_railway_cli() {
    if ! command_exists railway; then
        echo "📦 Installing Railway CLI..."
        npm install -g @railway/cli
        echo "✅ Railway CLI installed"
    else
        echo "✅ Railway CLI already installed"
    fi
}

# Function to check authentication
check_auth() {
    if railway whoami &> /dev/null; then
        echo "✅ Authenticated with Railway"
        return 0
    else
        echo "❌ Not authenticated with Railway"
        return 1
    fi
}

# Function to authenticate with token
auth_with_token() {
    echo "🔐 Attempting to authenticate with token..."
    
    # Create Railway config directory
    mkdir -p ~/.railway
    
    # Create config with token
    cat > ~/.railway/config.json << EOF
{
  "projects": {},
  "user": {
    "token": "$RAILWAY_TOKEN"
  },
  "lastUpdateCheck": "$(date -u +"%Y-%m-%dT%H:%M:%S.000000000Z")",
  "newVersionAvailable": null,
  "linkedFunctions": null
}
EOF
    
    echo "✅ Token configured"
}

# Function to deploy via CLI
deploy_via_cli() {
    echo "🔧 Deploying via Railway CLI..."
    
    # Check if project is linked
    if [ ! -f ".railway/project.json" ]; then
        echo "🔗 Creating new project..."
        railway init --name "$PROJECT_NAME"
    fi
    
    # Deploy
    echo "🚀 Deploying application..."
    railway up
    
    echo "✅ Deployment completed!"
}

# Function to deploy via Docker
deploy_via_docker() {
    echo "🐳 Deploying via Docker..."
    
    # Build Docker image
    echo "🔨 Building Docker image..."
    docker build -t genx-fx-trading .
    
    echo "✅ Docker image built successfully"
    echo "📝 To deploy to Railway with Docker:"
    echo "   1. Push to Docker Hub: docker push your-username/genx-fx-trading"
    echo "   2. Use Railway's Docker deployment option"
}

# Function to show manual deployment steps
show_manual_steps() {
    echo "📋 Manual Deployment Steps"
    echo "=========================="
    echo ""
    echo "1. Go to Railway Dashboard: https://railway.app/dashboard"
    echo "2. Click 'New Project'"
    echo "3. Choose 'Deploy from GitHub repo'"
    echo "4. Select your repository"
    echo "5. Configure environment variables:"
    echo "   - NODE_ENV=production"
    echo "   - PYTHON_VERSION=3.11"
    echo "   - PORT=8000"
    echo "6. Deploy!"
    echo ""
    echo "🔗 Your Railway token: $RAILWAY_TOKEN"
}

# Function to show API deployment
show_api_deployment() {
    echo "🔌 API Deployment via Railway API"
    echo "================================="
    echo ""
    echo "Create project:"
    echo "curl -H \"Authorization: Bearer $RAILWAY_TOKEN\" \\"
    echo "  -H \"Content-Type: application/json\" \\"
    echo "  -d '{\"query\":\"mutation { projectCreate(input: { name: \\\"$PROJECT_NAME\\\" }) { project { id } } }\"}' \\"
    echo "  https://backboard.railway.app/graphql/v2"
    echo ""
    echo "Then use: railway link <PROJECT_ID> && railway up"
}

# Main deployment menu
show_menu() {
    echo "Choose deployment method:"
    echo "1. Railway CLI (automatic)"
    echo "2. Railway CLI with manual login"
    echo "3. Docker deployment"
    echo "4. Manual deployment via web interface"
    echo "5. API deployment"
    echo "6. Show all options"
    echo "0. Exit"
    echo ""
    read -p "Enter your choice (0-6): " choice
}

# Main execution
main() {
    install_railway_cli
    
    while true; do
        show_menu
        
        case $choice in
            1)
                echo ""
                echo "🔄 Option 1: Railway CLI (automatic)"
                echo "===================================="
                auth_with_token
                if check_auth; then
                    deploy_via_cli
                else
                    echo "❌ Authentication failed. Try option 2."
                fi
                break
                ;;
            2)
                echo ""
                echo "🔄 Option 2: Railway CLI with manual login"
                echo "=========================================="
                echo "Please login to Railway:"
                echo "railway login"
                echo ""
                echo "After login, run: ./deploy_to_railway.sh"
                break
                ;;
            3)
                echo ""
                echo "🔄 Option 3: Docker deployment"
                echo "=============================="
                deploy_via_docker
                break
                ;;
            4)
                echo ""
                echo "🔄 Option 4: Manual deployment via web interface"
                echo "==============================================="
                show_manual_steps
                break
                ;;
            5)
                echo ""
                echo "🔄 Option 5: API deployment"
                echo "==========================="
                show_api_deployment
                break
                ;;
            6)
                echo ""
                echo "🔄 Option 6: Show all options"
                echo "============================"
                echo ""
                echo "📋 All Deployment Options:"
                echo "=========================="
                echo ""
                echo "🔧 Option 1: Railway CLI (automatic)"
                echo "   - Uses token authentication"
                echo "   - Fully automated deployment"
                echo ""
                echo "🔧 Option 2: Railway CLI with manual login"
                echo "   - Interactive login required"
                echo "   - Most reliable method"
                echo ""
                echo "🔧 Option 3: Docker deployment"
                echo "   - Builds Docker image"
                echo "   - Deploy to any container platform"
                echo ""
                echo "🔧 Option 4: Manual deployment via web interface"
                echo "   - Use Railway dashboard"
                echo "   - Visual configuration"
                echo ""
                echo "🔧 Option 5: API deployment"
                echo "   - Direct API calls"
                echo "   - Programmatic deployment"
                echo ""
                echo "🎯 Recommended: Option 2 (Railway CLI with manual login)"
                echo ""
                ;;
            0)
                echo "👋 Goodbye!"
                exit 0
                ;;
            *)
                echo "❌ Invalid choice. Please enter 0-6."
                ;;
        esac
    done
}

# Run main function
main