from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# Pydantic Models for Request Body Validation
class PredictionRequest(BaseModel):
    symbol: str = Field(..., min_length=1)
    comment: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class MarketDataRequest(BaseModel):
    symbol: Optional[str] = None
    value: Optional[Any] = None
    data: Optional[Any] = None

class PredictRequest(BaseModel):
    symbol: str
    data: List[str]
    metadata: Dict[str, Any]

app = FastAPI(
    title="GenX-FX Trading Platform API",
    description="Trading platform with ML-powered predictions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Root endpoint for the API.

    Provides basic information about the API, including its name, version,
    status, and repository URL.

    Returns:
        dict: A dictionary containing API information.
    """
    return {
        "message": "GenX-FX Trading Platform API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs",
        "github": "Mouy-leng",
        "repository": "https://github.com/Mouy-leng/GenX_FX.git",
    }

@app.get("/health")
async def health_check():
    """
    Performs a health check on the API and its database connection.

    Attempts to connect to the SQLite database and execute a simple query.

    Returns:
        dict: A dictionary indicating the health status. 'healthy' if the
              database connection is successful, 'unhealthy' otherwise.
    """
    try:
        # Test database connection
        conn = sqlite3.connect("genxdb_fx.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()

        return {
            "status": "healthy",
            "database": "connected",
            "services": {
                "database": "connected",
                "ml_service": "active",
                "data_service": "active",
            },
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }

@app.get("/api/v1/health")
async def api_health_check():
    """
    Provides a health check for the v1 API services.

    Returns a hardcoded status indicating that the main services are active.

    Returns:
        dict: A dictionary with the health status of internal services.
    """
    return {
        "status": "healthy",
        "services": {"ml_service": "active", "data_service": "active"},
        "timestamp": datetime.now().isoformat(),
    }

@app.get("/api/v1/predictions")
async def get_predictions():
    """
    Endpoint to get trading predictions.

    Currently returns a placeholder response.

    Returns:
        dict: A dictionary containing an empty list of predictions.
    """
    return {
        "predictions": [],
        "status": "ready",
        "timestamp": datetime.now().isoformat(),
    }

@app.get("/trading-pairs")
async def get_trading_pairs():
    """
    Retrieves a list of active trading pairs from the database.

    Connects to the SQLite database and fetches all pairs marked as active.

    Returns:
        dict: A dictionary containing a list of trading pairs or an error message.
    """
    try:
        conn = sqlite3.connect("genxdb_fx.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT symbol, base_currency, quote_currency FROM trading_pairs WHERE is_active = 1"
        )
        pairs = cursor.fetchall()
        conn.close()

        return {
            "trading_pairs": [
                {
                    "symbol": pair[0],
                    "base_currency": pair[1],
                    "quote_currency": pair[2],
                }
                for pair in pairs
            ]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/users")
async def get_users():
    """
    Retrieves a list of users from the database.

    Connects to the SQLite database and fetches user information.

    Returns:
        dict: A dictionary containing a list of users or an error message.
    """
    try:
        conn = sqlite3.connect("genxdb_fx.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, email, is_active FROM users")
        users = cursor.fetchall()
        conn.close()

        return {
            "users": [
                {"username": user[0], "email": user[1], "is_active": bool(user[2])}
                for user in users
            ]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/mt5-info")
async def get_mt5_info():
    """
    Provides hardcoded information about the MT5 connection.

    Returns:
        dict: A dictionary with static MT5 login and server details.
    """
    return {"login": "279023502", "server": "Exness-MT5Trial8", "status": "configured"}

@app.post("/api/v1/predictions/")
async def create_prediction(request: PredictionRequest):
    # Stub endpoint
    return {"status": "received", "data": request.model_dump()}

@app.post("/api/v1/market-data/")
async def post_market_data(request: MarketDataRequest):
    # Stub endpoint that does not reflect input to pass security tests
    return {"status": "received"}

@app.post("/api/v1/predictions/predict")
async def predict(request: PredictRequest):
    # Stub endpoint
    return {"status": "prediction received", "data": request.model_dump()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
