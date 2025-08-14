from fastapi import FastAPI
import os
from datetime import datetime

app = FastAPI(title="GenX AMP System", version="1.0.0")

@app.get("/")
async def root():
    return {
        "message": "GenX AMP Trading System", 
        "version": "1.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/status")
async def api_status():
    return {
        "api": "running",
        "project_id": os.getenv("GCP_PROJECT_ID", "unknown"),
        "bucket": os.getenv("BUCKET_NAME", "not_configured")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
