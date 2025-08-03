#!/bin/bash

# Railway Deployment Script for GenX FX Trading System
# Uses Railway API directly to deploy the application

set -e

# Railway configuration
RAILWAY_TOKEN="b82dcb0b-b5da-41ba-9541-7aac3471eb96"
RAILWAY_API_URL="https://backboard.railway.app/graphql/v2"
PROJECT_NAME="genx-fx-trading"

echo "🚀 Starting Railway deployment for GenX FX Trading System..."

# Check authentication
echo "🔐 Checking authentication..."
USER_INFO=$(curl -s -H "Authorization: Bearer $RAILWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { me { id name email } }"}' \
  "$RAILWAY_API_URL")

if echo "$USER_INFO" | grep -q "errors"; then
    echo "❌ Authentication failed"
    echo "$USER_INFO"
    exit 1
fi

# Extract user name using grep and sed
USER_NAME=$(echo "$USER_INFO" | grep -o '"name":"[^"]*"' | sed 's/"name":"//;s/"//')
echo "✅ Authenticated as: $USER_NAME"

# List existing projects
echo "📋 Checking existing projects..."
PROJECTS_RESPONSE=$(curl -s -H "Authorization: Bearer $RAILWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { projects { nodes { id name description } } }"}' \
  "$RAILWAY_API_URL")

if echo "$PROJECTS_RESPONSE" | grep -q "errors"; then
    echo "❌ Failed to list projects"
    echo "$PROJECTS_RESPONSE"
    exit 1
fi

# Check if project already exists using grep
PROJECT_ID=$(echo "$PROJECTS_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | sed 's/"id":"//;s/"//')

if [ -n "$PROJECT_ID" ]; then
    echo "✅ Found existing project: $PROJECT_NAME"
else
    echo "📦 Creating new project: $PROJECT_NAME"
    CREATE_RESPONSE=$(curl -s -H "Authorization: Bearer $RAILWAY_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"query":"mutation { projectCreate(input: { name: \"'$PROJECT_NAME'\", description: \"GenX FX Trading System - AI-powered Forex trading platform\" }) { project { id name } } }"}' \
      "$RAILWAY_API_URL")
    
    if echo "$CREATE_RESPONSE" | grep -q "errors"; then
        echo "❌ Failed to create project"
        echo "$CREATE_RESPONSE"
        exit 1
    fi
    
    PROJECT_ID=$(echo "$CREATE_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | sed 's/"id":"//;s/"//')
    echo "✅ Created project with ID: $PROJECT_ID"
fi

echo "🎉 Railway project setup complete!"
echo "📊 Project ID: $PROJECT_ID"

# Now let's try to use the Railway CLI to link and deploy
echo "🔗 Attempting to link project with Railway CLI..."

# Create a simple configuration file
mkdir -p .railway
echo "{\"projectId\":\"$PROJECT_ID\"}" > .railway/project.json

# Try to link the project
if railway link "$PROJECT_ID" 2>/dev/null; then
    echo "✅ Successfully linked project"
    
    # Deploy the application
    echo "🚀 Deploying application..."
    if railway up; then
        echo "✅ Deployment successful!"
        echo "🌐 Your application should be available at the Railway URL"
    else
        echo "❌ Deployment failed"
        exit 1
    fi
else
    echo "⚠️  Could not link project automatically"
    echo "📝 Manual steps required:"
    echo "1. Run: railway login"
    echo "2. Run: railway link $PROJECT_ID"
    echo "3. Run: railway up"
    echo ""
    echo "🔧 Or you can deploy manually using:"
    echo "railway up --project $PROJECT_ID"
fi

echo "🎉 Railway deployment process completed!"