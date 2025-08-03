# Manual Railway Deployment Guide for GenX FX Trading System

## 🚀 Quick Deployment Steps

Since you're already logged in as **KEA MOUYLENG**, follow these steps:

### Step 1: Create New Project
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Choose **"Deploy from GitHub repo"** (recommended)
   - Or choose **"Start from scratch"** if you want to upload files manually

### Step 2: Configure Project
1. **Project Name**: `genx-fx-trading`
2. **Repository**: Select your GitHub repository (if using GitHub)
3. **Branch**: `main` or `master`

### Step 3: Railway Will Automatically Detect
- ✅ **Dockerfile** - Multi-stage container build
- ✅ **railway.json** - Railway configuration
- ✅ **api/main.py** - FastAPI application
- ✅ **package.json** - Node.js dependencies
- ✅ **requirements-prod.txt** - Python dependencies

### Step 4: Environment Variables (Optional)
Add these in Railway dashboard if needed:
```
NODE_ENV=production
PYTHON_VERSION=3.11
PORT=8000
```

### Step 5: Deploy
1. Click **"Deploy"**
2. Railway will automatically:
   - Build the Docker container
   - Install dependencies
   - Start the application
   - Provide a public URL

## 🐳 Container Configuration

Your project is configured for containerized deployment:

### Dockerfile Structure
```dockerfile
# Frontend Build Stage (Node.js 18)
FROM node:18-alpine AS frontend-builder
# Builds React frontend

# Backend Build Stage (Python 3.11)
FROM python:3.11-slim AS backend-builder
# Installs Python dependencies

# Production Stage
FROM python:3.11-slim
# Runs FastAPI application on port 8000
```

### Application Structure
```
/
├── api/main.py              # FastAPI application entry point
├── client/                  # React frontend source
├── core/                    # Python backend core
├── utils/                   # Utility functions
├── config/                  # Configuration files
├── Dockerfile               # Multi-stage container build
├── railway.json             # Railway configuration
├── package.json             # Node.js dependencies
└── requirements-prod.txt    # Production Python dependencies
```

## 🔧 Railway Configuration

Your `railway.json` is configured for:
- **Builder**: Dockerfile
- **Health Check**: `/health` endpoint
- **Port**: 8000
- **Restart Policy**: On failure with 10 retries

## 📊 Post-Deployment

### Check Your Application
1. **Health Check**: `https://your-app.railway.app/health`
2. **API Documentation**: `https://your-app.railway.app/docs`
3. **Frontend**: `https://your-app.railway.app/`

### Monitor Your Application
- **Logs**: View in Railway dashboard
- **Metrics**: Monitor resource usage
- **Deployments**: Track deployment history

### Common Commands (if CLI works)
```bash
# Check status
railway status

# View logs
railway logs

# Open dashboard
railway open

# Get domain
railway domain
```

## 🚨 Troubleshooting

### Build Failures
1. Check Railway build logs
2. Verify all dependencies are in requirements files
3. Ensure Dockerfile syntax is correct

### Application Not Starting
1. Check application logs
2. Verify port configuration (should use `$PORT`)
3. Test health endpoint

### Environment Variables
1. Set required environment variables in Railway dashboard
2. Ensure sensitive data is properly configured

## 🎯 Your Railway Token
```
b82dcb0b-b5da-41ba-9541-7aac3471eb96
```

## 📞 Support
- Railway Documentation: https://docs.railway.app/
- Railway Status: https://status.railway.app/
- Your Account: KEA MOUYLENG

## 🎉 Success!
Once deployed, your GenX FX Trading System will be available at:
`https://your-app-name.railway.app/`

The application includes:
- ✅ FastAPI backend with AI trading algorithms
- ✅ React frontend with modern UI
- ✅ Containerized deployment
- ✅ Health monitoring
- ✅ Automatic scaling