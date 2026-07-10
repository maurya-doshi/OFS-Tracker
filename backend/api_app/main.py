import os
import logging
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Determine a writable data directory BEFORE importing any app.* module ────
# This runs first so pydantic-settings picks up DATABASE_URL when config.py
# is imported for the first time.
def _find_data_dir() -> str:
    candidates = [
        "/app/data",                          # Docker (root user, WORKDIR /app)
        os.path.join(os.getcwd(), "data"),    # Nixpacks / relative CWD
        "/tmp/ofs_data",                       # Always writable fallback
    ]
    for path in candidates:
        try:
            os.makedirs(path, exist_ok=True)
            probe = os.path.join(path, ".write_probe")
            with open(probe, "w") as f:
                f.write("ok")
            os.remove(probe)
            logger.info(f"OFS data directory: {path}")
            return path
        except OSError as exc:
            logger.warning(f"Directory {path!r} not writable: {exc}")
    fallback = tempfile.mkdtemp(prefix="ofs_data_")
    logger.warning(f"All candidates failed — using temp dir: {fallback}")
    return fallback

_DATA_DIR = _find_data_dir()
# FORCE overwrite DATABASE_URL. If Railway injected a Postgres URL, setdefault() would 
# keep it, causing create_engine to crash because psycopg2 isn't installed.
os.environ["DATABASE_URL"] = f"sqlite:///{_DATA_DIR}/ofs_tracker.db"
logger.info(f"DATABASE_URL forcefully set to = {os.environ['DATABASE_URL']}")

# ── App imports (config.py reads DATABASE_URL env var above) ─────────────────
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_app.database.database import engine, Base
from api_app.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified.")
    except Exception as e:
        logger.error(f"Failed to initialise database: {e}")

    try:
        from api_app.scheduler import start_scheduler, shutdown_scheduler
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

app.include_router(router.api_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "OFS Tracker API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/health")
def api_health_check():
    return {"status": "ok"}
