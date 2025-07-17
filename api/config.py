from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
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
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
