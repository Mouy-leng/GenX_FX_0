#!/bin/bash

# Railway Native Container Deployment for GenX FX Trading System
# Uses Railway's built-in containerization

set -e

RAILWAY_TOKEN="b82dcb0b-b5da-41ba-9541-7aac3471eb96"
PROJECT_NAME="genx-fx-trading"

echo "🚀 Railway Native Container Deployment for GenX FX Trading System"
echo "================================================================="
echo ""

# Function to check if Railway CLI is available
check_railway() {
    if ! command -v railway &> /dev/null; then
        echo "📦 Installing Railway CLI..."
        npm install -g @railway/cli
    fi
    echo "✅ Railway CLI is available"
}

# Function to authenticate with Railway
authenticate_railway() {
    echo "🔐 Checking Railway authentication..."
    if railway whoami &> /dev/null; then
        echo "✅ Already authenticated with Railway"
        USER_INFO=$(railway whoami)
        echo "   Logged in as: $USER_INFO"
    else
        echo "⚠️  Not authenticated. Please login:"
        echo "   railway login"
        echo ""
        echo "   After login, run this script again."
        exit 1
    fi
}

# Function to check project configuration
check_configuration() {
    echo "🔧 Checking project configuration..."
    
    # Check if railway.json exists
    if [ -f "railway.json" ]; then
        echo "✅ railway.json found"
    else
        echo "❌ railway.json not found"
        exit 1
    fi
    
    # Check if Dockerfile exists
    if [ -f "Dockerfile" ]; then
        echo "✅ Dockerfile found"
    else
        echo "❌ Dockerfile not found"
        exit 1
    fi
    
    # Check if main application files exist
    if [ -f "api/main.py" ]; then
        echo "✅ FastAPI main.py found"
    else
        echo "❌ api/main.py not found"
        exit 1
    fi
    
    if [ -f "package.json" ]; then
        echo "✅ package.json found"
    else
        echo "❌ package.json not found"
        exit 1
    fi
}

# Function to create or link project
setup_project() {
    echo "📦 Setting up Railway project..."
    
    # Check if project is already linked
    if [ -f ".railway/project.json" ]; then
        echo "✅ Project already linked"
        PROJECT_ID=$(cat .railway/project.json | grep -o '"projectId":"[^"]*"' | sed 's/"projectId":"//;s/"//')
        echo "   Project ID: $PROJECT_ID"
    else
        echo "🔗 Creating new Railway project..."
        railway init --name "$PROJECT_NAME"
        echo "✅ Project created and linked"
    fi
}

# Function to deploy to Railway
deploy_to_railway() {
    echo "🚀 Deploying to Railway..."
    echo "   This will use Railway's built-in containerization"
    echo "   based on the Dockerfile and railway.json configuration"
    echo ""
    
    # Deploy using Railway
    echo "📤 Uploading and deploying..."
    railway up
    
    if [ $? -eq 0 ]; then
        echo "✅ Deployment successful!"
    else
        echo "❌ Deployment failed"
        exit 1
    fi
}

# Function to show deployment info
show_deployment_info() {
    echo ""
    echo "🎉 Deployment completed successfully!"
    echo "===================================="
    echo ""
    echo "📊 Check deployment status:"
    echo "   railway status"
    echo ""
    echo "📋 View logs:"
    echo "   railway logs"
    echo ""
    echo "🌐 Open dashboard:"
    echo "   railway open"
    echo ""
    echo "🔗 Get your application URL:"
    echo "   railway domain"
    echo ""
    echo "📈 Monitor your application:"
    echo "   railway metrics"
    echo ""
    echo "🔧 Manage environment variables:"
    echo "   railway variables"
}

# Function to show manual steps
show_manual_steps() {
    echo ""
    echo "📋 Manual Deployment Steps"
    echo "=========================="
    echo ""
    echo "1. Ensure you're logged in:"
    echo "   railway login"
    echo ""
    echo "2. Create new project (if needed):"
    echo "   railway init --name $PROJECT_NAME"
    echo ""
    echo "3. Deploy:"
    echo "   railway up"
    echo ""
    echo "4. Check status:"
    echo "   railway status"
    echo ""
    echo "5. View logs:"
    echo "   railway logs"
    echo ""
    echo "🔗 Your Railway token: $RAILWAY_TOKEN"
}

# Function to show project structure
show_project_structure() {
    echo ""
    echo "📁 Project Structure for Containerization"
    echo "========================================="
    echo ""
    echo "✅ railway.json - Railway configuration (Dockerfile builder)"
    echo "✅ Dockerfile - Multi-stage container build"
    echo "✅ api/main.py - FastAPI application entry point"
    echo "✅ package.json - Node.js dependencies and scripts"
    echo "✅ requirements-prod.txt - Production Python dependencies"
    echo "✅ client/ - React frontend source"
    echo "✅ core/ - Python backend core modules"
    echo "✅ utils/ - Utility functions"
    echo "✅ config/ - Configuration files"
    echo ""
    echo "🐳 Container Configuration:"
    echo "   - Frontend: Node.js 18 Alpine (build stage)"
    echo "   - Backend: Python 3.11 Slim (production stage)"
    echo "   - Port: 8000"
    echo "   - Health check: /health endpoint"
}

# Main execution
main() {
    echo "🔍 Checking prerequisites..."
    check_railway
    authenticate_railway
    
    echo ""
    echo "Choose deployment method:"
    echo "1. Full automated deployment"
    echo "2. Check configuration only"
    echo "3. Show project structure"
    echo "4. Show manual steps"
    echo "0. Exit"
    echo ""
    read -p "Enter your choice (0-4): " choice
    
    case $choice in
        1)
            echo ""
            echo "🔄 Full automated deployment"
            echo "============================"
            check_configuration
            setup_project
            deploy_to_railway
            show_deployment_info
            ;;
        2)
            echo ""
            echo "🔄 Check configuration only"
            echo "=========================="
            check_configuration
            show_project_structure
            ;;
        3)
            show_project_structure
            ;;
        4)
            show_manual_steps
            ;;
        0)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please enter 0-4."
            exit 1
            ;;
    esac
}

# Run main function
main