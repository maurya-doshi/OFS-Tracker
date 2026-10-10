import os
import logging
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Trust DATABASE_URL from the environment for deployment compatibility.

# ── App imports (config.py reads DATABASE_URL env var above) ─────────────────
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, Base
from api import endpoints


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified.")
    except Exception as e:
        logger.error(f"Failed to initialise database: {e}")

    try:
        from scheduler import start_scheduler, shutdown_scheduler
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api")


@app.get("/api/status")
def root():
    return {"message": "OFS Tracker API is running"}

from fastapi.staticfiles import StaticFiles

# Serve the static frontend
frontend_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "out")
if os.path.exists(frontend_out):
    app.mount("/", StaticFiles(directory=frontend_out, html=True), name="static")
else:
    logger.warning(f"Frontend static directory {frontend_out} not found. Static files will not be served.")
