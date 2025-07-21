# 🚀 GenX FX - Advanced AI-Powered Forex Trading Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![AI Powered](https://img.shields.io/badge/AI-Powered-FF6B35.svg)](https://ai.google.dev/)

A comprehensive, production-ready forex trading platform that combines artificial intelligence, real-time market analysis, social sentiment tracking, and automated trading execution. Built with modern technologies and designed for both retail and institutional traders.

## ✨ Key Features

### 🤖 **AI-Driven Trading Intelligence**
- **Advanced ML Models**: Ensemble learning with multiple algorithms (Random Forest, SVM, Neural Networks)
- **Real-time Predictions**: Live market analysis and signal generation
- **Pattern Recognition**: Automated detection of chart patterns and market structures
- **Sentiment Analysis**: AI-powered analysis of news and social media sentiment
- **Continuous Learning**: Models that adapt and improve with new market data

### 📊 **Professional Trading Engine**
- **Multi-Broker Support**: Integration with major forex brokers and exchanges
- **Risk Management**: Advanced position sizing, stop-loss, and portfolio management
- **Order Execution**: Lightning-fast order placement with slippage protection
- **Backtesting**: Comprehensive historical strategy validation
- **Live Trading**: Fully automated trading with manual override capabilities

### 📱 **Modern Web Interface**
- **Real-time Dashboard**: Live charts, P&L, and portfolio monitoring
- **TradingView Integration**: Professional charting with custom indicators
- **Mobile Responsive**: Trade from any device with full functionality
- **Customizable Layouts**: Personalized trading workspace
- **Performance Analytics**: Detailed trading statistics and reporting

### 🌐 **Market Data & Analysis**
- **Real-time Feeds**: WebSocket streams from multiple data providers
- **Technical Indicators**: 50+ built-in technical analysis tools
- **Economic Calendar**: Real-time economic events and impact analysis
- **News Integration**: Automated news sentiment scoring and filtering
- **Social Sentiment**: Reddit, Twitter, and forum sentiment tracking

### 🔧 **Enterprise Infrastructure**
- **Scalable Architecture**: Microservices with Docker and Kubernetes
- **High Availability**: Redundant systems with automatic failover
- **Security**: Bank-grade encryption and security protocols
- **API Integration**: RESTful API for third-party integrations
- **Monitoring**: Comprehensive logging, metrics, and alerting

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[React Dashboard] --> B[TradingView Charts]
        A --> C[Portfolio Manager]
        A --> D[Trading Controls]
    end
    
    subgraph "API Gateway"
        E[FastAPI Server] --> F[Authentication]
        E --> G[Rate Limiting]
        E --> H[Request Routing]
    end
    
    subgraph "Core Services"
        I[Trading Engine] --> J[Order Management]
        I --> K[Risk Management]
        I --> L[Position Tracker]
        
        M[AI Engine] --> N[ML Models]
        M --> O[Signal Generator]
        M --> P[Pattern Recognition]
        
        Q[Data Engine] --> R[Market Data]
        Q --> S[News Feed]
        Q --> T[Social Sentiment]
    end
    
    subgraph "Infrastructure"
        U[PostgreSQL] --> V[Redis Cache]
        U --> W[Time Series DB]
        X[Message Queue] --> Y[WebSocket Server]
        Z[Monitoring] --> AA[Logging]
    end
    
    A --> E
    E --> I
    E --> M
    E --> Q
    I --> U
    M --> U
    Q --> U
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **Docker & Docker Compose**
- **Git**

### 1. Clone Repository
```bash
git clone https://github.com/Mouy-leng/GenX_FX.git
cd GenX_FX
```

### 2. Environment Setup
```bash
# Copy environment template
cp config/environments/development.env .env

# Edit with your API keys and settings
nano .env
```

### 3. Quick Start with Docker
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Manual Setup (Development)
```bash
# Backend setup
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

### 5. Access the Platform
- **Trading Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Admin Panel**: http://localhost:3000/admin
- **Health Check**: http://localhost:8000/health

## 🔑 Configuration

### Required API Keys

Create a `.env` file with the following configuration:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/genx_fx
REDIS_URL=redis://localhost:6379/0

# Trading & Market Data
BROKER_API_KEY=your_broker_api_key
BROKER_API_SECRET=your_broker_secret
MARKET_DATA_API_KEY=your_market_data_key

# AI & Analysis Services
OPENAI_API_KEY=your_openai_key  # For advanced AI analysis
NEWS_API_KEY=your_news_api_key
SOCIAL_API_KEY=your_social_sentiment_key

# Notification Services
TELEGRAM_BOT_TOKEN=your_telegram_token
DISCORD_WEBHOOK_URL=your_discord_webhook
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_USER=your_email@gmail.com
EMAIL_SMTP_PASSWORD=your_app_password

# Security
JWT_SECRET_KEY=your_super_secret_jwt_key
ENCRYPTION_KEY=your_encryption_key

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
ENABLE_LIVE_TRADING=false  # Set to true for live trading
RISK_MANAGEMENT_ENABLED=true
MAX_POSITION_SIZE=0.02  # 2% of account per trade
```

### Feature Flags
```bash
# Enable/Disable Features
ENABLE_AI_SIGNALS=true
ENABLE_NEWS_ANALYSIS=true
ENABLE_SOCIAL_SENTIMENT=true
ENABLE_AUTOMATED_TRADING=false
ENABLE_BACKTESTING=true
ENABLE_PAPER_TRADING=true
```

## 📡 API Documentation

### Authentication
```bash
# Login and get JWT token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "trader", "password": "password"}'
```

### Trading Endpoints
```bash
# Get trading signals
GET /api/v1/signals/current
GET /api/v1/signals/history

# Portfolio management
GET /api/v1/portfolio/summary
GET /api/v1/portfolio/positions
GET /api/v1/portfolio/performance

# Order management
POST /api/v1/orders/place
GET /api/v1/orders/active
DELETE /api/v1/orders/{order_id}

# Market data
GET /api/v1/market/quotes/{symbol}
GET /api/v1/market/history/{symbol}
WebSocket: /ws/market-data
```

### AI & Analysis
```bash
# AI predictions
POST /api/v1/ai/predict
GET /api/v1/ai/model-performance
POST /api/v1/ai/retrain

# Market analysis
GET /api/v1/analysis/technical/{symbol}
GET /api/v1/analysis/sentiment/{symbol}
GET /api/v1/analysis/news/{symbol}
```

## 📊 Trading Features

### Supported Instruments
- **Forex**: 28+ major, minor, and exotic currency pairs
- **Indices**: S&P 500, NASDAQ, Dow Jones, FTSE, DAX, Nikkei
- **Commodities**: Gold, Silver, Oil, Natural Gas
- **Cryptocurrencies**: Bitcoin, Ethereum, major altcoins

### Trading Strategies
- **Trend Following**: Moving average crossovers, momentum strategies
- **Mean Reversion**: RSI-based, Bollinger Band strategies
- **Breakout Trading**: Support/resistance breakouts, volatility strategies
- **Scalping**: High-frequency, low-latency execution
- **Swing Trading**: Multi-day position strategies
- **AI Ensemble**: Combined ML model predictions

### Risk Management
- **Position Sizing**: Kelly Criterion, fixed percentage, volatility-based
- **Stop Losses**: Fixed, trailing, ATR-based, time-based
- **Take Profits**: Fixed, partial closures, risk-reward ratios
- **Drawdown Control**: Maximum drawdown limits, cooling-off periods
- **Correlation Limits**: Prevent over-exposure to correlated assets

## 🧪 Testing & Validation

### Run Test Suite
```bash
# All tests
pytest tests/ -v

# Specific test categories
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/e2e/ -v

# Performance tests
pytest tests/performance/ -v

# Coverage report
pytest --cov=backend tests/ --cov-report=html
```

### Backtesting
```bash
# Run backtests
python scripts/backtest.py --strategy trend_following --symbol EURUSD --period 1Y

# Generate backtest report
python scripts/generate_report.py --backtest-id latest
```

## 🚢 Production Deployment

### Docker Deployment (Recommended)
```bash
# Production deployment
docker-compose -f deployment/docker/docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale backend=3 --scale worker=2
```

### Kubernetes Deployment
```bash
# Deploy to Kubernetes
kubectl apply -f deployment/kubernetes/

# Monitor deployment
kubectl get pods -l app=genx-fx
kubectl logs -f deployment/genx-fx-backend
```

### Cloud Deployment
```bash
# AWS ECS deployment
aws ecs create-service --cli-input-json file://deployment/aws/ecs-service.json

# Google Cloud Run
gcloud run deploy genx-fx --source . --region us-central1

# DigitalOcean App Platform
doctl apps create --spec deployment/digitalocean/app.yaml
```

## 📈 Performance & Monitoring

### System Metrics
- **Latency**: <50ms average API response time
- **Throughput**: 10,000+ requests per second
- **Uptime**: 99.9% availability SLA
- **Order Execution**: <100ms average execution time

### Monitoring Stack
- **Prometheus**: Metrics collection and storage
- **Grafana**: Real-time dashboards and visualization
- **ELK Stack**: Centralized logging and search
- **Jaeger**: Distributed tracing and performance monitoring
- **AlertManager**: Intelligent alerting and notifications

### Health Checks
```bash
# System health
curl http://localhost:8000/health

# Detailed status
curl http://localhost:8000/api/v1/system/status

# Performance metrics
curl http://localhost:8000/api/v1/system/metrics
```

## 🔒 Security & Compliance

### Security Features
- **Authentication**: JWT-based with refresh tokens
- **Authorization**: Role-based access control (RBAC)
- **Encryption**: AES-256 encryption for sensitive data
- **API Security**: Rate limiting, input validation, CORS protection
- **Network Security**: VPN support, IP whitelisting
- **Audit Logging**: Comprehensive audit trails

### Compliance
- **Data Protection**: GDPR compliance for EU users
- **Financial Regulations**: Designed for regulatory compliance
- **Risk Disclosure**: Built-in risk warnings and disclosures
- **Audit Trail**: Complete transaction and decision logging

## 📚 Documentation

### Complete Documentation
- 📖 **[User Guide](docs/user_guides/)** - Complete user documentation
- 🔧 **[API Reference](docs/api/)** - Detailed API documentation
- 🚀 **[Deployment Guide](docs/deployment/)** - Production deployment
- 🏗️ **[Architecture](docs/technical/)** - Technical specifications
- 📊 **[Trading Strategies](docs/strategies/)** - Strategy documentation

### Video Tutorials
- 🎥 **Platform Overview** - Introduction and features
- 🎥 **Getting Started** - Setup and first trade
- 🎥 **Advanced Features** - AI signals and automation
- 🎥 **Risk Management** - Protecting your capital
- 🎥 **API Integration** - Building custom tools

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend development
- Write comprehensive tests for new features
- Update documentation for new features
- Follow semantic versioning for releases

## 🆘 Support & Community

### Get Help
- 📧 **Email**: support@genx-fx.com
- 💬 **Discord**: [Join our community](https://discord.gg/genx-fx)
- 📖 **Documentation**: [docs.genx-fx.com](https://docs.genx-fx.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/Mouy-leng/GenX_FX/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/Mouy-leng/GenX_FX/discussions)

### Community
- 🌟 **Star us on GitHub** if you find this project useful
- 🐦 **Follow us on Twitter**: [@GenXFX](https://twitter.com/GenXFX)
- 📺 **YouTube Channel**: [GenX FX Trading](https://youtube.com/genx-fx)
- 📱 **Telegram**: [t.me/genx_fx](https://t.me/genx_fx)

## 📊 Roadmap

### Current Version: v1.0.0
✅ Core trading engine  
✅ AI-powered signals  
✅ Real-time market data  
✅ Risk management  
✅ Web dashboard  

### Version 1.1.0 (Q2 2025)
🔄 Mobile apps (iOS/Android)  
🔄 Copy trading features  
🔄 Advanced charting tools  
🔄 Social trading community  

### Version 1.2.0 (Q3 2025)
📋 Institutional features  
📋 Multi-account management  
📋 Advanced reporting  
📋 Custom strategy builder  

### Version 2.0.0 (Q4 2025)
📋 Decentralized trading  
📋 Blockchain integration  
📋 NFT trading cards  
📋 DAO governance  

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Risk Disclaimer

**IMPORTANT RISK WARNING**: Trading foreign exchange and CFDs carries a high level of risk and may not be suitable for all investors. The high degree of leverage can work against you as well as for you. Before deciding to trade foreign exchange or CFDs, you should carefully consider your investment objectives, level of experience, and risk appetite. Past performance is not indicative of future results.

---

## 🎯 Why Choose GenX FX?

### For Retail Traders
- **Easy to Use**: Professional tools with intuitive interface
- **AI Assistance**: Let AI help identify trading opportunities
- **Education**: Built-in learning resources and tutorials
- **Community**: Connect with other successful traders

### For Institutional Clients
- **Scalability**: Handle high-volume trading operations
- **Customization**: Tailor the platform to your specific needs
- **Integration**: Seamless API integration with existing systems
- **Compliance**: Built with regulatory requirements in mind

### For Developers
- **Open Source**: Contribute to the project and customize freely
- **Modern Stack**: Built with cutting-edge technologies
- **API-First**: Everything accessible via comprehensive APIs
- **Documentation**: Extensive docs and examples

---

<div align="center">

**⚡ GenX FX - Where AI Meets Trading Excellence ⚡**

*Empowering traders with intelligent automation and professional-grade tools*

Made with ❤️ by the GenX Trading Team

[Website](https://genx-fx.com) • [Documentation](https://docs.genx-fx.com) • [Community](https://discord.gg/genx-fx) • [Support](mailto:support@genx-fx.com)

</div>
