from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class PredictionRequest(BaseModel):
    symbol: str
    data: Optional[Any] = None
    comment: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class MarketDataRequest(BaseModel):
    symbol: Optional[str] = None
    data: Optional[Any] = None
    value: Optional[Any] = None