# 🚀 GenX FX Trading System

**Advanced AI-Powered Forex Signal Generator for MT4/5 Expert Advisors**

GenX FX is a sophisticated trading system that uses ensemble machine learning models to generate high-quality forex trading signals. Designed specifically to feed signals to MetaTrader 4/5 Expert Advisors through Excel/CSV files.

## 🏗️ System Architecture

```mermaid
graph TB
    %% User Interface Layer
    subgraph "User Interface"
        CLI[AMP CLI]
        WEB[Web Dashboard]
        API[REST API]
    end

    %% Authentication Layer
    subgraph "Authentication"
        AUTH[Token Auth]
        SESSION[Session Mgmt]
        USER[User Context]
    end

    %% Core Services Layer
    subgraph "Core Services"
        JOB_RUNNER[Job Runner]
        SCHEDULER[Scheduler]
        MONITOR[Monitor]
    end

    %% Integration Layer
    subgraph "Integrations"
        GEMINI[Gemini AI]
        REDDIT[Reddit Signals]
        NEWS[News Aggregator]
        WEBSOCKET[WebSocket Streams]
    end

    %% Data Layer
    subgraph "Data Sources"
        FXCM[FXCM API]
        BYBIT[Bybit API]
        NEWS_API[News APIs]
        REDDIT_API[Reddit API]
    end

    %% Processing Layer
    subgraph "Processing"
        AI_ENGINE[AI Engine]
        SIGNAL_GEN[Signal Generator]
        RISK_MGMT[Risk Management]
        VALIDATION[Signal Validation]
    end

    %% Output Layer
    subgraph "Output"
        EXCEL[Excel Dashboard]
        CSV_MT4[MT4 CSV]
        CSV_MT5[MT5 CSV]
        JSON_API[JSON API]
    end

    %% Infrastructure Layer
    subgraph "Infrastructure"
        DOCKER[Docker Container]
        DB[(Database)]
        REDIS[(Redis Cache)]
        LOGS[Logs]
    end

    %% Connections
    CLI --> AUTH
    WEB --> AUTH
    API --> AUTH
    
    AUTH --> USER
    USER --> JOB_RUNNER
    USER --> SCHEDULER
    USER --> MONITOR
    
    JOB_RUNNER --> GEMINI
    JOB_RUNNER --> REDDIT
    JOB_RUNNER --> NEWS
    JOB_RUNNER --> WEBSOCKET
    
    GEMINI --> AI_ENGINE
    REDDIT --> SIGNAL_GEN
    NEWS --> SIGNAL_GEN
    WEBSOCKET --> SIGNAL_GEN
    
    FXCM --> SIGNAL_GEN
    BYBIT --> SIGNAL_GEN
    NEWS_API --> NEWS
    REDDIT_API --> REDDIT
    
    SIGNAL_GEN --> AI_ENGINE
    AI_ENGINE --> RISK_MGMT
    RISK_MGMT --> VALIDATION
    VALIDATION --> EXCEL
    VALIDATION --> CSV_MT4
    VALIDATION --> CSV_MT5
    VALIDATION --> JSON_API
    
    DOCKER --> DB
    DOCKER --> REDIS
    DOCKER --> LOGS
    
    %% Styling
    classDef userInterface fill:#e1f5fe
    classDef auth fill:#fff3e0
    classDef core fill:#f3e5f5
    classDef integration fill:#e8f5e8
    classDef data fill:#fff8e1
    classDef processing fill:#fce4ec
    classDef output fill:#e0f2f1
    classDef infrastructure fill:#f1f8e9
    
    class CLI,WEB,API userInterface
    class AUTH,SESSION,USER auth
    class JOB_RUNNER,SCHEDULER,MONITOR core
    class GEMINI,REDDIT,NEWS,WEBSOCKET integration
    class FXCM,BYBIT,NEWS_API,REDDIT_API data
    class AI_ENGINE,SIGNAL_GEN,RISK_MGMT,VALIDATION processing
    class EXCEL,CSV_MT4,CSV_MT5,JSON_API output
    class DOCKER,DB,REDIS,LOGS infrastructure
```

## 🔄 Workflow Diagram

```mermaid
flowchart TD
    START([Start AMP System]) --> AUTH{Authenticated?}
    AUTH -->|No| LOGIN[Login with Token]
    AUTH -->|Yes| INIT[Initialize Services]
    LOGIN --> INIT
    
    INIT --> SCHEDULE{Start Scheduler?}
    SCHEDULE -->|Yes| SCHEDULER[Start Job Scheduler]
    SCHEDULE -->|No| MANUAL[Manual Job Execution]
    
    SCHEDULER --> WAIT[Wait for Next Job]
    MANUAL --> RUN_JOB[Run Next Job]
    WAIT --> RUN_JOB
    
    RUN_JOB --> COLLECT[Collect Market Data]
    COLLECT --> GATHER[Gather News & Sentiment]
    GATHER --> AI_PREDICT[Generate AI Predictions]
    AI_PREDICT --> SIGNALS[Generate Trading Signals]
    SIGNALS --> VALIDATE[Validate Signals]
    
    VALIDATE --> EXECUTE{Execute Trades?}
    EXECUTE -->|Yes| TRADE[Execute Trades]
    EXECUTE -->|No| REPORT[Generate Reports]
    TRADE --> REPORT
    
    REPORT --> LOG[Log Results]
    LOG --> MONITOR[Update Monitoring]
    MONITOR --> NEXT{Continue?}
    NEXT -->|Yes| WAIT
    NEXT -->|No| STOP([Stop System])
    
    %% Styling
    classDef startEnd fill:#ff9999
    classDef process fill:#99ccff
    classDef decision fill:#ffcc99
    classDef data fill:#99ff99
    
    class START,STOP startEnd
    class LOGIN,INIT,SCHEDULER,MANUAL,RUN_JOB,COLLECT,GATHER,AI_PREDICT,SIGNALS,TRADE,REPORT,LOG,MONITOR process
    class AUTH,SCHEDULE,EXECUTE,NEXT decision
    class WAIT data
```

## 🐳 Docker Deployment Architecture

```mermaid
graph TB
    subgraph "Docker Host"
        subgraph "AMP Trading System"
            AMP[AMP Container<br/>mouyleng/mouy-leng:latest]
        end
        
        subgraph "Supporting Services"
            REDIS[Redis Cache]
            POSTGRES[PostgreSQL DB]
            GRAFANA[Grafana Dashboard]
        end
        
        subgraph "External APIs"
            DOCKER_HUB[Docker Hub<br/>mouyleng/mouy-leng]
            GITHUB[GitHub Actions<br/>Auto Build & Push]
        end
    end
    
    subgraph "External Services"
        FXCM_API[FXCM API]
        BYBIT_API[Bybit API]
        GEMINI_API[Gemini AI API]
        REDDIT_API[Reddit API]
        NEWS_API[News APIs]
    end
    
    subgraph "Output Files"
        EXCEL[Excel Dashboard]
        CSV[CSV Signals]
        JSON[JSON API]
        LOGS[System Logs]
    end
    
    %% Connections
    GITHUB --> DOCKER_HUB
    DOCKER_HUB --> AMP
    
    AMP --> REDIS
    AMP --> POSTGRES
    AMP --> GRAFANA
    
    AMP --> FXCM_API
    AMP --> BYBIT_API
    AMP --> GEMINI_API
    AMP --> REDDIT_API
    AMP --> NEWS_API
    
    AMP --> EXCEL
    AMP --> CSV
    AMP --> JSON
    AMP --> LOGS
    
    %% Styling
    classDef container fill:#e3f2fd
    classDef service fill:#f3e5f5
    classDef external fill:#e8f5e8
    classDef output fill:#fff3e0
    
    class AMP container
    class REDIS,POSTGRES,GRAFANA,DOCKER_HUB,GITHUB service
    class FXCM_API,BYBIT_API,GEMINI_API,REDDIT_API,NEWS_API external
    class EXCEL,CSV,JSON,LOGS output
```

## ✨ Key Features

### 🤖 **Advanced AI Engine**
- **Ensemble Learning**: Combines 5+ ML models (Random Forest, XGBoost, LightGBM, SVM, Neural Networks)
- **Multi-Timeframe Analysis**: M15, H1, H4, D1 confluence validation
- **Dynamic Feature Engineering**: 50+ technical indicators and market microstructure features
- **Real-time Model Training**: Automatic retraining every 24 hours
- **Confidence Scoring**: Advanced signal validation and strength assessment

### 📊 **Signal Output for MT4/5**
- **Excel Dashboard**: Professional formatted Excel with color coding and charts
- **MT4 CSV**: Simplified format optimized for MT4 EAs
- **MT5 CSV**: Enhanced format with additional metadata for MT5 EAs
- **JSON API**: Real-time signal data for custom integrations
- **Automatic Updates**: Real-time signal refresh every 30 seconds

### 🛡️ **Risk Management**
- **Position Sizing**: Dynamic position sizing based on volatility and risk parameters
- **ATR-Based Stops**: Adaptive stop-loss and take-profit levels
- **Risk/Reward Validation**: Minimum 1.5:1 risk-reward ratio
- **Market Condition Awareness**: Volatility and trend-based adjustments
- **Multi-Symbol Risk Control**: Maximum exposure limits across all pairs

### 💹 **Market Coverage**
- **7 Major Pairs**: EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, USDCAD, NZDUSD
- **Multiple Timeframes**: M15, H1, H4, D1 analysis
- **Session Awareness**: London, New York, Asian session optimization
- **Economic Calendar Integration**: (Optional) Fundamental analysis overlay

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/genx-fx-trading.git
cd genx-fx-trading

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p config logs signal_output ai_models
```

### 2. Configuration

Edit `config/trading_config.json`:

```json
{
  "fxcm": {
    "use_mock": true,  // Set to false for real FXCM data
    "access_token": "your_fxcm_token"
  },
  "risk_management": {
    "max_risk_per_trade": 0.02,  // 2% risk per trade
    "max_total_risk": 0.06       // 6% total portfolio risk
  }
}
```

### 3. Run the System

```bash
# Generate sample signals for testing
python main.py sample --count 5

# Train AI models with historical data
python main.py train --symbols EURUSD GBPUSD

# Run live signal generation
python main.py live

# Run backtesting
python main.py backtest --start-date 2023-01-01 --end-date 2024-01-01
```

## 📈 Signal Output Files

The system generates several files in the `signal_output/` directory:

### 📊 **Excel Dashboard** (`genx_signals.xlsx`)
- **Active Signals**: Current trading opportunities
- **Signal History**: Historical signal performance
- **Performance Metrics**: Win rates, confidence averages
- **Summary Dashboard**: System status and statistics

### 📋 **MT4 Signals** (`MT4_Signals.csv`)
```csv
Magic,Symbol,Signal,EntryPrice,StopLoss,TakeProfit,LotSize,Timestamp
123456,EURUSD,BUY,1.10500,1.10300,1.10900,0.02,2024-01-15 14:30:00
```

### 📋 **MT5 Signals** (`MT5_Signals.csv`)
```csv
Magic,Symbol,Signal,EntryPrice,StopLoss,TakeProfit,Volume,Confidence,RiskReward,Expiry,Comment
123456,EURUSD,BUY,1.10500,1.10300,1.10900,0.02,0.78,2.0,2024-01-15 18:30:00,GenX_UPTREND_STRONG
```

## 🔧 MT4/5 EA Integration

### Sample MT4 EA Code

```mql4
// Read signals from CSV file
string filename = "MT4_Signals.csv";
int file = FileOpen(filename, FILE_READ|FILE_CSV);

if(file != INVALID_HANDLE) {
    while(!FileIsEnding(file)) {
        string magic = FileReadString(file);
        string symbol = FileReadString(file);
        string signal = FileReadString(file);
        double entry = FileReadNumber(file);
        double sl = FileReadNumber(file);
        double tp = FileReadNumber(file);
        double lots = FileReadNumber(file);
        
        // Execute trade based on signal
        if(symbol == Symbol() && signal == "BUY") {
            OrderSend(Symbol(), OP_BUY, lots, Ask, 3, sl, tp, "GenX Signal", magic);
        }
    }
    FileClose(file);
}
```

## 🎯 System Modes

### **Live Trading** 
```bash
python main.py live
```
- Continuous signal generation
- Real-time market data processing
- Automatic file updates every 30 seconds
- Performance monitoring and logging

### **Training Mode**
```bash
python main.py train --symbols EURUSD GBPUSD --timeframes H1 H4
```
- Download historical data
- Train ensemble ML models
- Cross-validation and performance metrics
- Model serialization and storage

### **Backtesting**
```bash
python main.py backtest --start-date 2023-01-01 --end-date 2024-01-01
```
- Historical strategy testing
- Performance metrics calculation
- Sharpe ratio, max drawdown, win rate analysis
- Trade-by-trade results

### **Testing**
```bash
python main.py test
```
- System component validation
- Data provider connectivity tests
- AI model prediction tests
- Signal generation verification

## 📊 Performance Metrics

The system tracks comprehensive performance metrics:

- **Signal Accuracy**: Prediction success rate
- **Risk-Adjusted Returns**: Sharpe ratio, Calmar ratio
- **Drawdown Analysis**: Maximum and average drawdowns
- **Win Rate**: Percentage of profitable signals
- **Risk/Reward**: Average risk-reward ratios
- **Model Performance**: Individual model contributions

## 🔧 Advanced Configuration

### **AI Model Tuning**
```json
{
  "ai_models": {
    "ensemble_size": 5,
    "retrain_interval_hours": 24,
    "confidence_threshold_dynamic": true,
    "models": {
      "random_forest": {"enabled": true, "n_estimators": 100},
      "xgboost": {"enabled": true, "learning_rate": 0.1},
      "lightgbm": {"enabled": true, "max_depth": 6}
    }
  }
}
```

### **Risk Management**
```json
{
  "risk_management": {
    "max_risk_per_trade": 0.02,
    "position_sizing_method": "fixed_fractional",
    "stop_loss_method": "atr_based",
    "volatility_adjustment": true
  }
}
```

### **Signal Validation**
```json
{
  "validation": {
    "timeframe_confluence_required": 2,
    "technical_confluence_threshold": 3,
    "multi_timeframe_validation": true
  }
}
```

## 🔌 FXCM Integration

For real market data, configure FXCM credentials:

```json
{
  "fxcm": {
    "use_mock": false,
    "environment": "demo",  // or "real"
    "access_token": "your_fxcm_access_token",
    "server_url": "https://api-fxpractice.fxcm.com"
  }
}
```

1. **Get FXCM Token**: Register at [FXCM](https://www.fxcm.com/) and get API access
2. **Demo Account**: Start with demo environment for testing
3. **Rate Limits**: System automatically handles FXCM API rate limits

## 📈 Strategy Overview

### **Signal Generation Process**
1. **Data Collection**: Real-time/historical price data from FXCM
2. **Feature Engineering**: Technical indicators, price patterns, time features
3. **Multi-Timeframe Analysis**: H1 primary with M15, H4, D1 confirmation
4. **AI Prediction**: Ensemble of 5 ML models with confidence scoring
5. **Signal Validation**: Risk/reward, confluence, market condition checks
6. **Output Generation**: Excel, CSV, JSON files for MT4/5 consumption

### **Risk Management Process**
1. **Position Sizing**: Based on account balance and risk percentage
2. **Stop Loss**: ATR-based adaptive stops
3. **Take Profit**: 2:1 minimum risk/reward ratio
4. **Market Conditions**: Volatility and trend adjustments
5. **Exposure Limits**: Maximum concurrent positions per symbol

## 🐛 Troubleshooting

### **Common Issues**

**No signals generated:**
```bash
# Check system status
python main.py test

# Verify configuration
cat config/trading_config.json

# Check logs
tail -f logs/genx_trading.log
```

**FXCM connection issues:**
- Verify access token in config
- Check demo vs real environment setting
- Ensure FXCM API limits aren't exceeded

**Missing dependencies:**
```bash
# Install TA-Lib (required for technical analysis)
# On Ubuntu/Debian:
sudo apt-get install libta-lib-dev
pip install ta-lib

# On macOS:
brew install ta-lib
pip install ta-lib
```

## 📁 Project Structure

```
genx-fx-trading/
├── main.py                    # Main application entry point
├── config/
│   └── trading_config.json    # System configuration
├── core/
│   ├── trading_engine.py      # Main trading engine
│   ├── spreadsheet_manager.py # Signal output management
│   ├── ai_models/
│   │   └── ensemble_predictor.py  # AI ensemble system
│   └── data_sources/
│       └── fxcm_provider.py   # FXCM data provider
├── signal_output/             # Generated signal files
│   ├── genx_signals.xlsx      # Excel dashboard
│   ├── MT4_Signals.csv        # MT4 format
│   ├── MT5_Signals.csv        # MT5 format
│   └── genx_signals.json      # JSON format
├── ai_models/                 # Trained ML models
├── logs/                      # System logs
└── requirements.txt           # Python dependencies
```

## 🚀 Next Steps

1. **Setup & Test**: Install and run sample signal generation
2. **MT4/5 Integration**: Create EA to read CSV signals
3. **Paper Trading**: Test with demo account
4. **Model Training**: Train on recent historical data
5. **Live Trading**: Deploy with real account (at your own risk)

## ⚠️ Disclaimer

**This software is for educational and research purposes only. Trading forex involves substantial risk and may not be suitable for all investors. Past performance does not guarantee future results. Always use proper risk management and never risk more than you can afford to lose.**

## 📧 Support

For questions and support:
- 📧 Email: support@genx-fx.com
- 💬 Discord: [GenX Trading Community](https://discord.gg/genx-trading)
- 📖 Documentation: [docs.genx-fx.com](https://docs.genx-fx.com)

---

**Made with ❤️ for the trading community**
