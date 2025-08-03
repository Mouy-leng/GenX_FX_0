# Railway Deployment Guide for GenX FX Trading System

## Overview
This guide will help you deploy the GenX FX Trading System to Railway. The application consists of:
- **Backend**: FastAPI Python application (`api/main.py`)
- **Frontend**: React application with Vite
- **Database**: PostgreSQL (configured via Railway)

## Prerequisites
- Railway account with token: `b82dcb0b-b5da-41ba-9541-7aac3471eb96`
- Railway CLI installed: `npm install -g @railway/cli`

## Method 1: Automated Deployment (Recommended)

### Step 1: Setup Project Configuration
The project is already configured with:
- `railway.json` - Railway configuration
- `package.json` - Node.js dependencies and scripts
- `requirements.txt` - Python dependencies
- `api/main.py` - FastAPI application entry point

### Step 2: Login to Railway
```bash
# Interactive login (recommended)
railway login

# Or browserless login
railway login --browserless
```

### Step 3: Create and Link Project
```bash
# Create new project
railway init --name genx-fx-trading

# Or link to existing project (if you have a project ID)
railway link <PROJECT_ID>
```

### Step 4: Deploy Application
```bash
# Deploy the entire application
railway up

# Check deployment status
railway status

# View logs
railway logs
```

## Method 2: Manual Deployment via Web Interface

### Step 1: Create Project on Railway Dashboard
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Choose "Deploy from GitHub repo" or "Start from scratch"
4. Name the project: `genx-fx-trading`

### Step 2: Configure Services
1. **API Service (Backend)**:
   - Add service: "Python"
   - Source: Your GitHub repository
   - Root directory: `/` (or specify if needed)
   - Build command: `pip install -r requirements-prod.txt`
   - Start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

2. **Web Service (Frontend)**:
   - Add service: "Node.js"
   - Source: Your GitHub repository
   - Root directory: `/` (or specify if needed)
   - Build command: `npm install && npm run build`
   - Start command: `npm run preview` or serve the `dist` folder

### Step 3: Set Environment Variables
Add these environment variables in Railway dashboard:

```bash
# Database
DATABASE_URL=your_postgresql_url

# API Keys (if needed)
GEMINI_API_KEY=your_gemini_key
REDDIT_CLIENT_ID=your_reddit_client_id
NEWSDATA_API_KEY=your_news_api_key

# Application Settings
NODE_ENV=production
PYTHON_VERSION=3.11
PORT=8000

# CORS Settings
ALLOWED_ORIGINS=https://your-domain.railway.app
```

## Method 3: Using Railway API Directly

### Step 1: Create Project via API
```bash
curl -H "Authorization: Bearer b82dcb0b-b5da-41ba-9541-7aac3471eb96" \
  -H "Content-Type: application/json" \
  -d '{"query":"mutation { projectCreate(input: { name: \"genx-fx-trading\" }) { project { id } } }"}' \
  https://backboard.railway.app/graphql/v2
```

### Step 2: Deploy via CLI
```bash
# After getting project ID from step 1
railway link <PROJECT_ID>
railway up
```

## Application Structure

```
/
├── api/                    # FastAPI backend
│   ├── main.py            # Main FastAPI app
│   ├── routers/           # API routes
│   ├── services/          # Business logic
│   └── config.py          # Configuration
├── client/                # React frontend
│   ├── src/               # Source code
│   ├── public/            # Static files
│   └── package.json       # Frontend dependencies
├── services/              # Node.js services
│   └── server/            # Express server
├── railway.json           # Railway configuration
├── package.json           # Root package.json
├── requirements.txt       # Python dependencies
└── requirements-prod.txt  # Production Python dependencies
```

## Deployment Commands

### Build Commands
```bash
# Install dependencies
npm install
pip install -r requirements-prod.txt

# Build frontend
npm run build

# Start backend
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

### Railway Commands
```bash
# Deploy
railway up

# View status
railway status

# View logs
railway logs

# Open dashboard
railway open

# Set variables
railway variables set KEY=VALUE

# Connect to database
railway connect
```

## Troubleshooting

### Common Issues

1. **Authentication Error**:
   ```bash
   # Re-login to Railway
   railway logout
   railway login
   ```

2. **Build Failures**:
   - Check `railway.json` configuration
   - Verify all dependencies are in `requirements.txt`/`package.json`
   - Check build logs: `railway logs`

3. **Port Issues**:
   - Ensure application uses `$PORT` environment variable
   - Check Railway service configuration

4. **Database Connection**:
   - Verify `DATABASE_URL` is set correctly
   - Check database service is running

### Debug Commands
```bash
# Check Railway status
railway status

# View recent deployments
railway deployments

# Check environment variables
railway variables

# View service logs
railway logs --service api
railway logs --service web
```

## Post-Deployment

### Verify Deployment
1. Check application health: `https://your-app.railway.app/health`
2. Test API endpoints: `https://your-app.railway.app/docs`
3. Verify frontend loads correctly

### Monitor Application
- Use Railway dashboard for monitoring
- Set up alerts for service failures
- Monitor resource usage

### Scale Application
- Adjust service resources in Railway dashboard
- Add more instances if needed
- Configure auto-scaling rules

## Support

If you encounter issues:
1. Check Railway documentation: https://docs.railway.app/
2. View application logs: `railway logs`
3. Check Railway status page: https://status.railway.app/