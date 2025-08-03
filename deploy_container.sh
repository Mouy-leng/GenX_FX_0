#!/bin/bash

# Containerized Railway Deployment Script for GenX FX Trading System

set -e

RAILWAY_TOKEN="b82dcb0b-b5da-41ba-9541-7aac3471eb96"
PROJECT_NAME="genx-fx-trading"
IMAGE_NAME="genx-fx-trading"

echo "🐳 Containerized Railway Deployment for GenX FX Trading System"
echo "=============================================================="
echo ""

# Function to check if Docker is available
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed or not available"
        echo "Please install Docker first: https://docs.docker.com/get-docker/"
        exit 1
    fi
    echo "✅ Docker is available"
}

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
    else
        echo "⚠️  Not authenticated. Please login:"
        echo "   railway login"
        echo ""
        echo "   After login, run this script again."
        exit 1
    fi
}

# Function to build Docker image
build_docker_image() {
    echo "🔨 Building Docker image..."
    echo "   Image name: $IMAGE_NAME"
    echo "   Dockerfile: Dockerfile"
    echo ""
    
    # Build the image
    docker build -t $IMAGE_NAME .
    
    if [ $? -eq 0 ]; then
        echo "✅ Docker image built successfully"
    else
        echo "❌ Docker build failed"
        exit 1
    fi
}

# Function to test Docker image locally
test_docker_image() {
    echo "🧪 Testing Docker image locally..."
    
    # Run the container in background
    CONTAINER_ID=$(docker run -d -p 8000:8000 --name genx-test $IMAGE_NAME)
    
    if [ $? -eq 0 ]; then
        echo "✅ Container started successfully"
        
        # Wait a bit for the application to start
        echo "⏳ Waiting for application to start..."
        sleep 10
        
        # Test health endpoint
        if curl -f http://localhost:8000/health &> /dev/null; then
            echo "✅ Health check passed"
        else
            echo "⚠️  Health check failed, but continuing..."
        fi
        
        # Stop and remove test container
        docker stop $CONTAINER_ID
        docker rm $CONTAINER_ID
        echo "🧹 Test container cleaned up"
    else
        echo "❌ Failed to start test container"
        exit 1
    fi
}

# Function to deploy to Railway
deploy_to_railway() {
    echo "🚀 Deploying to Railway..."
    
    # Check if project is linked
    if [ ! -f ".railway/project.json" ]; then
        echo "🔗 Creating new Railway project..."
        railway init --name "$PROJECT_NAME"
    fi
    
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
}

# Function to show manual container deployment steps
show_manual_steps() {
    echo ""
    echo "📋 Manual Container Deployment Steps"
    echo "===================================="
    echo ""
    echo "1. Build Docker image:"
    echo "   docker build -t $IMAGE_NAME ."
    echo ""
    echo "2. Test locally:"
    echo "   docker run -p 8000:8000 $IMAGE_NAME"
    echo ""
    echo "3. Push to Docker Hub (optional):"
    echo "   docker tag $IMAGE_NAME your-username/$IMAGE_NAME"
    echo "   docker push your-username/$IMAGE_NAME"
    echo ""
    echo "4. Deploy to Railway:"
    echo "   railway up"
    echo ""
    echo "5. Or use Railway's Docker deployment:"
    echo "   - Go to Railway Dashboard"
    echo "   - Create new project"
    echo "   - Choose 'Deploy from Dockerfile'"
    echo "   - Upload your code or connect GitHub repo"
}

# Main execution
main() {
    echo "🔍 Checking prerequisites..."
    check_docker
    check_railway
    authenticate_railway
    
    echo ""
    echo "Choose deployment method:"
    echo "1. Full automated deployment (build + test + deploy)"
    echo "2. Build and test only"
    echo "3. Deploy only (assumes image is built)"
    echo "4. Show manual steps"
    echo "0. Exit"
    echo ""
    read -p "Enter your choice (0-4): " choice
    
    case $choice in
        1)
            echo ""
            echo "🔄 Full automated deployment"
            echo "============================"
            build_docker_image
            test_docker_image
            deploy_to_railway
            show_deployment_info
            ;;
        2)
            echo ""
            echo "🔄 Build and test only"
            echo "======================"
            build_docker_image
            test_docker_image
            ;;
        3)
            echo ""
            echo "🔄 Deploy only"
            echo "=============="
            deploy_to_railway
            show_deployment_info
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