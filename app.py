import sys
import os
import logging

# ── Ensure backend/ is on the Python path ─────────────────────────────────────
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Find writable data dir & set DATABASE_URL BEFORE any backend import ───────
# api_app.database.database reads settings (which reads DATABASE_URL) at import.
def _find_data_dir() -> str:
    candidates = [
        "/home/user/app/data",           # HF Spaces (user 1000)
        os.path.join(os.getcwd(), "data"),
        "/tmp/ofs_data",
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
            logger.warning(f"{path!r} not writable: {exc}")
    import tempfile
    fallback = tempfile.mkdtemp(prefix="ofs_data_")
    logger.warning(f"All candidates failed — using temp dir: {fallback}")
    return fallback

_DATA_DIR = _find_data_dir()
os.environ["DATABASE_URL"] = f"sqlite:///{_DATA_DIR}/ofs_tracker.db"
logger.info(f"DATABASE_URL = {os.environ['DATABASE_URL']}")

# ── Backend imports ────────────────────────────────────────────────────────────
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_app.database.database import engine, Base
from api_app.api import router
from api_app.scheduler import start_scheduler, shutdown_scheduler

# ── Build a FRESH FastAPI app — NO lifespan= parameter ────────────────────────
# CRITICAL: mount_gradio_app internally calls @app.on_event("startup").
# In Starlette 0.40+ (FastAPI 0.115.x), mixing lifespan= AND on_event on the
# same app raises ValueError. A fresh app with no lifespan= avoids this.
fastapi_app = FastAPI(title="OFS Live Bid Tracker API")

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_app.include_router(router.api_router, prefix="/api")

@fastapi_app.get("/health")
def health_check():
    return {"status": "ok"}

@fastapi_app.get("/api/health")
def api_health():
    return {"status": "ok"}

@fastapi_app.get("/api/status")
def api_status():
    return {"message": "OFS Tracker API is running"}

# Use on_event — compatible with mount_gradio_app which also adds on_event handlers.
# DO NOT use lifespan= on fastapi_app: Starlette 0.40+ raises ValueError if
# both lifespan= and on_event are present on the same app.
@fastapi_app.on_event("startup")
async def _startup():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified.")
    except Exception as e:
        logger.error(f"DB init failed: {e}")
    try:
        start_scheduler()
    except Exception as e:
        logger.error(f"Scheduler start failed: {e}")

@fastapi_app.on_event("shutdown")
async def _shutdown():
    try:
        shutdown_scheduler()
    except Exception as e:
        logger.error(f"Scheduler shutdown failed: {e}")

# ── Gradio UI ─────────────────────────────────────────────────────────────────
import gradio as gr

with gr.Blocks(title="OFS Tracker API") as _blocks:
    gr.Markdown("# 📈 OFS Tracker API")
    gr.Markdown(
        "The FastAPI backend is running behind this Gradio Space.\n\n"
        "**API Endpoints:**\n"
        "- `GET /api/issues` — list all tracked OFS issues\n"
        "- `GET /health` — health check\n"
        "- `GET /docs` — interactive API documentation"
    )

# mount_gradio_app also uses @fastapi_app.on_event("startup") internally.
# Both sets of handlers run — no conflict because fastapi_app has no lifespan=.
app = gr.mount_gradio_app(fastapi_app, _blocks, path="/")
