import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment or fallback to 8000
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting uvicorn on 0.0.0.0:{port}...")
    uvicorn.run("api_app.main:app", host="0.0.0.0", port=port, log_level="info")
