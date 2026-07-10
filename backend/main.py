# Proxy to app.main for environments that hardcode `uvicorn main:app` or `python main.py`
from backend.app.main import app
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting uvicorn on 0.0.0.0:{port} via proxy main.py...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
