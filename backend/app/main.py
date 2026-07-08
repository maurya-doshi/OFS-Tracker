import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.api import router

logger = logging.getLogger(__name__)

# Ensure the data directory exists for SQLite at the absolute path Railway uses
os.makedirs("/app/data", exist_ok=True)
logger.info("Data directory: /app/data")

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
