import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.api import router

logger = logging.getLogger(__name__)

# Ensure the data directory exists for SQLite — computed relative to this file
# so it works regardless of CWD or container environment
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_BASE_DIR, "data")
os.makedirs(_DATA_DIR, exist_ok=True)
logger.info(f"Data directory: {_DATA_DIR}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    # Create DB tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified.")
    except Exception as e:
        logger.error(f"Failed to initialise database: {e}")

    # Start background scheduler
    try:
        from app.scheduler import start_scheduler, shutdown_scheduler
        start_scheduler()
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
        shutdown_scheduler = lambda: None  # noqa: E731

    yield

    # --- Shutdown ---
    try:
        shutdown_scheduler()
    except Exception as e:
        logger.error(f"Error during scheduler shutdown: {e}")

app = FastAPI(title="OFS Live Bid Tracker API", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "OFS Tracker API is running"}
