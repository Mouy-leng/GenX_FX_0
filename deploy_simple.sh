#!/bin/bash

# Simple Railway Deployment Script for GenX FX Trading System

echo "🚀 GenX FX Trading System - Railway Deployment"
echo "=============================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

echo "✅ Railway CLI is installed"

# Check authentication
echo "🔐 Checking Railway authentication..."
if railway whoami &> /dev/null; then
    echo "✅ Already authenticated with Railway"
else
    echo "⚠️  Not authenticated. Please login:"
    echo "   railway login"
    echo ""
    echo "   Or use browserless login:"
    echo "   railway login --browserless"
    echo ""
    echo "   After login, run this script again."
    exit 1
fi

# Create or link project
echo "📦 Setting up Railway project..."
if [ -f ".railway/project.json" ]; then
    echo "✅ Project already linked"
else
    echo "🔗 Creating new project..."
    railway init --name genx-fx-trading
fi

# Deploy the application
echo "🚀 Deploying application to Railway..."
railway up

echo "✅ Deployment completed!"
echo ""
echo "📊 Check deployment status:"
echo "   railway status"
echo ""
echo "📋 View logs:"
echo "   railway logs"
echo ""
echo "🌐 Open dashboard:"
echo "   railway open"