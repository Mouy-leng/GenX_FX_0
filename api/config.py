from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"  # Allow extra fields in .env file
    )
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GenX-EA Trading Platform"
    VERSION: str = "2.0.0"
    DESCRIPTION: str = "Advanced AI-powered trading platform with real-time market analysis"
    
    # Database
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/trading_db")
    MONGODB_URL: Optional[str] = os.getenv("MONGODB_URL", "mongodb://localhost:27017/trading_db")
    
    # Redis for caching
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # AI Model Configuration
    MODEL_PATH: str = "ai_models/market_predictor.joblib"
    ENSEMBLE_MODEL_PATH: str = "ai_models/ensemble_model.joblib"
    
    # Trading Configuration
    DEFAULT_SYMBOL: str = "BTCUSDT"
    MAX_POSITION_SIZE: float = 0.1
    RISK_PERCENTAGE: float = 0.02
    
    # External APIs
    BYBIT_API_KEY: Optional[str] = os.getenv("BYBIT_API_KEY")
    BYBIT_API_SECRET: Optional[str] = os.getenv("BYBIT_API_SECRET")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    NEWS_API_KEY: Optional[str] = os.getenv("NEWS_API_KEY")
    NEWSDATA_API_KEY: Optional[str] = os.getenv("NEWSDATA_API_KEY")
    ALPHAVANTAGE_API_KEY: Optional[str] = os.getenv("ALPHAVANTAGE_API_KEY")
    FINNHUB_API_KEY: Optional[str] = os.getenv("FINNHUB_API_KEY")
    
    # Social Media APIs
    REDDIT_CLIENT_ID: Optional[str] = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET: Optional[str] = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USERNAME: Optional[str] = os.getenv("REDDIT_USERNAME")
    REDDIT_PASSWORD: Optional[str] = os.getenv("REDDIT_PASSWORD")
    REDDIT_USER_AGENT: Optional[str] = os.getenv("REDDIT_USER_AGENT")
    
    # Notification Services
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_USER_ID: Optional[str] = os.getenv("TELEGRAM_USER_ID")
    GMAIL_USER: Optional[str] = os.getenv("GMAIL_USER")
    GMAIL_PASSWORD: Optional[str] = os.getenv("GMAIL_PASSWORD")
    GMAIL_APP_API_KEY: Optional[str] = os.getenv("GMAIL_APP_API_KEY")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    JWT_SECRET_KEY: Optional[str] = os.getenv("JWT_SECRET_KEY")
    CRYPTION_KEY: Optional[str] = os.getenv("CRYPTION_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"

settings = Settings()
