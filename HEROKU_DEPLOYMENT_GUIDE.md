# 🚀 GenX FX Trading System - Heroku Deployment Guide

## 🎯 Overview

This guide will help you deploy the GenX FX Trading System to **Heroku cloud** for 24/7 automated trading with your **Exness MT4/MT5 account**.

### **🏗️ Architecture on Heroku**
```
┌─────────────────────────────────┐
│         Heroku Cloud            │
│                                 │
│  ┌─────────────────────────────┐│
│  │      GenX AI Backend       ││
│  │   - AI Models              ││
│  │   - Signal Generation      ││
│  │   - PostgreSQL Database    ││
│  │   - Redis Cache            ││
│  └─────────────────────────────┘│
│                                 │
│  ┌─────────────────────────────┐│
│  │    Web API (REST)          ││
│  │   - Signal Endpoints       ││
│  │   - Health Monitoring      ││
│  │   - Dashboard API          ││
│  └─────────────────────────────┘│
└─────────────────────────────────┘
         │
         │ HTTPS API Calls
         ▼
┌─────────────────────────────────┐
│      Your Local Computer        │
│                                 │
│  ┌─────────────────────────────┐│
│  │     MT4/MT5 Terminal       ││
│  │   - GenX AI EA             ││
│  │   - Exness Account         ││
│  │   - Trade Execution        ││
│  └─────────────────────────────┘│
└─────────────────────────────────┘
```

## 📋 Prerequisites

### **1. Heroku Account**
- [Sign up for Heroku](https://signup.heroku.com/)
- Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

### **2. Exness Account**
- Active Exness trading account (demo or live)
- MT4 or MT5 terminal access
- Account credentials

### **3. GitHub Repository**
- Your GenX FX code pushed to GitHub
- Repository access for Heroku deployment

## 🚀 Step-by-Step Deployment

### **Step 1: Prepare Your Local Environment**

```bash
# 1. Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# 2. Login to Heroku
heroku login

# 3. Clone your repository (if not already done)
git clone https://github.com/your-username/GenX_FX.git
cd GenX_FX
```

### **Step 2: Create Heroku App**

```bash
# Create a new Heroku app
heroku create genx-fx-trading

# Set the buildpack for Python
heroku buildpacks:set heroku/python

# Add Redis addon (for caching)
heroku addons:create heroku-redis:hobby-dev

# Add PostgreSQL addon (for database)
heroku addons:create heroku-postgresql:hobby-dev
```

### **Step 3: Configure Environment Variables**

#### **Method 1: Using Heroku CLI**
```bash
# Set Exness credentials
heroku config:set EXNESS_LOGIN=your_exness_account_number
heroku config:set EXNESS_PASSWORD=your_exness_password
heroku config:set EXNESS_SERVER=Exness-MT5Trial8
heroku config:set EXNESS_ACCOUNT_TYPE=demo
heroku config:set EXNESS_TERMINAL=MT5

# Set trading parameters
heroku config:set MT5_SYMBOL=XAUUSD
heroku config:set MT5_TIMEFRAME=TIMEFRAME_M15
heroku config:set EA_MAGIC_NUMBER=12345
heroku config:set EA_DEFAULT_LOT_SIZE=0.01
heroku config:set EA_MAX_RISK_PER_TRADE=0.02

# Set security
heroku config:set SECRET_KEY=your-super-secret-key-here-minimum-32-characters
heroku config:set ACCESS_TOKEN_EXPIRE_MINUTES=30

# Set AI model parameters
heroku config:set MODEL_CONFIDENCE_THRESHOLD=0.7
heroku config:set SIGNAL_UPDATE_INTERVAL=300
heroku config:set MAX_SIGNALS_PER_HOUR=10

# Set trading strategies
heroku config:set GOLD_CONFIDENCE_THRESHOLD=0.75
heroku config:set GOLD_MAX_POSITION_SIZE=0.1
heroku config:set GOLD_STOP_LOSS_PIPS=50
heroku config:set GOLD_TAKE_PROFIT_PIPS=100

# Set performance parameters
heroku config:set MAX_CONCURRENT_TRADES=5
heroku config:set SIGNAL_CACHE_TTL=300
heroku config:set DATABASE_POOL_SIZE=10
heroku config:set REDIS_POOL_SIZE=5

# Set monitoring
heroku config:set LOG_LEVEL=INFO
heroku config:set ENABLE_METRICS=true
heroku config:set HEALTH_CHECK_INTERVAL=30
```

#### **Method 2: Using Heroku Dashboard**
1. Go to [Heroku Dashboard](https://dashboard.heroku.com/)
2. Select your app: `genx-fx-trading`
3. Go to **Settings** → **Config Vars**
4. Add each environment variable from the list above

### **Step 4: Create Required Files**

#### **Create `Procfile` for Heroku**
```bash
# Create Procfile
cat > Procfile << 'EOF'
web: python main.py
worker: python -m core.trading_engine
EOF
```

#### **Update `requirements.txt`**
```bash
# Ensure all dependencies are in requirements.txt
pip freeze > requirements.txt
```

#### **Create `runtime.txt`**
```bash
# Specify Python version
echo "python-3.11.7" > runtime.txt
```

### **Step 5: Deploy to Heroku**

```bash
# Add all files to git
git add .

# Commit changes
git commit -m "Setup for Heroku deployment"

# Push to Heroku
git push heroku main

# Scale the app
heroku ps:scale web=1
heroku ps:scale worker=1
```

### **Step 6: Verify Deployment**

```bash
# Check app status
heroku ps

# View logs
heroku logs --tail

# Open the app
heroku open
```

## 🔧 GitHub Secrets Setup

### **Required GitHub Secrets for CI/CD**

If you want to set up automatic deployment from GitHub, add these secrets in your repository:

1. Go to your GitHub repository
2. **Settings** → **Secrets and variables** → **Actions**
3. Add the following secrets:

#### **Heroku Secrets**
```
HEROKU_API_KEY=your_heroku_api_key
HEROKU_APP_NAME=genx-fx-trading
```

#### **Exness Trading Secrets**
```
EXNESS_LOGIN=your_exness_account_number
EXNESS_PASSWORD=your_exness_password
EXNESS_SERVER=Exness-MT5Trial8
EXNESS_ACCOUNT_TYPE=demo
EXNESS_TERMINAL=MT5
```

#### **Security Secrets**
```
SECRET_KEY=your-super-secret-key-here-minimum-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### **Trading Configuration Secrets**
```
MT5_SYMBOL=XAUUSD
MT5_TIMEFRAME=TIMEFRAME_M15
EA_MAGIC_NUMBER=12345
EA_DEFAULT_LOT_SIZE=0.01
EA_MAX_RISK_PER_TRADE=0.02
GOLD_CONFIDENCE_THRESHOLD=0.75
GOLD_MAX_POSITION_SIZE=0.1
GOLD_STOP_LOSS_PIPS=50
GOLD_TAKE_PROFIT_PIPS=100
```

## 📊 Monitoring & Management

### **Check App Status**
```bash
# View app info
heroku info

# Check dynos
heroku ps

# View recent logs
heroku logs --tail

# Monitor performance
heroku logs --source app
```

### **Database Management**
```bash
# Connect to PostgreSQL
heroku pg:psql

# View database info
heroku pg:info

# Backup database
heroku pg:backups:capture
```

### **Redis Management**
```bash
# Connect to Redis
heroku redis:cli

# View Redis info
heroku redis:info
```

## 🔄 Updating the App

### **Deploy Updates**
```bash
# Make your changes locally
git add .
git commit -m "Update trading logic"

# Deploy to Heroku
git push heroku main

# Restart the app if needed
heroku restart
```

### **Update Environment Variables**
```bash
# Update a single variable
heroku config:set NEW_VARIABLE=value

# View all variables
heroku config

# Update multiple variables
heroku config:set VAR1=value1 VAR2=value2
```

## 🎯 Integration with MT4/MT5 EA

### **1. EA Configuration**
Your MT4/MT5 EA needs to connect to the Heroku API:

```mql4
// In your EA, set the API endpoint
string API_BASE_URL = "https://genx-fx-trading.herokuapp.com/api/v1";
string API_KEY = "your-api-key";

// Fetch signals from Heroku
void FetchSignals() {
    string url = API_BASE_URL + "/signals/latest";
    // HTTP request to Heroku API
}
```

### **2. Signal Flow**
```
Heroku App → REST API → MT4/MT5 EA → Exness → Live Trading
```

## 🚨 Troubleshooting

### **Common Issues**

#### **1. App Crashes**
```bash
# Check logs
heroku logs --tail

# Restart app
heroku restart

# Check dyno status
heroku ps
```

#### **2. Database Connection Issues**
```bash
# Check database status
heroku pg:info

# Reset database if needed
heroku pg:reset DATABASE_URL
```

#### **3. Environment Variable Issues**
```bash
# Verify all variables are set
heroku config

# Check specific variable
heroku config:get EXNESS_LOGIN
```

### **Performance Optimization**

#### **Scale Dynos**
```bash
# Scale web dyno
heroku ps:scale web=2

# Scale worker dyno
heroku ps:scale worker=2
```

#### **Monitor Resources**
```bash
# Check dyno usage
heroku ps:scale

# View detailed metrics
heroku addons:open scout
```

## 📈 Cost Optimization

### **Heroku Pricing**
- **Hobby Dyno**: $7/month (basic)
- **Standard Dyno**: $25/month (recommended for trading)
- **PostgreSQL**: $5/month (hobby-dev)
- **Redis**: $15/month (hobby-dev)

### **Cost-Saving Tips**
1. Use **Hobby Dynos** for testing
2. **Scale down** during off-hours
3. Use **Standard Dynos** for production
4. Monitor usage with `heroku addons:open scout`

## ✅ Success Checklist

- [ ] Heroku app created and deployed
- [ ] Environment variables configured
- [ ] Database and Redis addons added
- [ ] App is running and accessible
- [ ] MT4/MT5 EA configured to connect
- [ ] Exness account credentials verified
- [ ] Trading signals are being generated
- [ ] Monitoring and logging set up
- [ ] Backup and recovery procedures tested

## 🎯 Next Steps

1. **Test with Demo Account**: Start with Exness demo account
2. **Monitor Performance**: Use Heroku logs and metrics
3. **Scale as Needed**: Upgrade dynos based on usage
4. **Implement Alerts**: Set up notifications for trading events
5. **Backup Strategy**: Regular database backups
6. **Security Review**: Audit API access and credentials

Your GenX FX trading system is now **running 24/7 on Heroku** and ready for automated trading with Exness! 🚀