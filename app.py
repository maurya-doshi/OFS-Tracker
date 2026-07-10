import sys
import os
import logging

# ── Ensure backend/ is on the Python path ────────────────────────────────────
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Find a writable data dir and set DATABASE_URL BEFORE any backend import ──
# (api_app.database.database reads settings at import time)
def _find_data_dir() -> str:
    candidates = [
        "/home/user/app/data",          # HF Spaces (runs as user 1000)
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
logger.info(f"DATABASE_URL set to: {os.environ['DATABASE_URL']}")

# ── Backend imports (safe now that DATABASE_URL is set) ──────────────────────
from fastapi.middleware.cors import CORSMiddleware
from api_app.database.database import engine, Base
from api_app.api import router
from api_app.scheduler import start_scheduler, shutdown_scheduler

# ── Gradio UI ─────────────────────────────────────────────────────────────────
import gradio as gr
from gradio.routes import App as GradioApp

with gr.Blocks(title="OFS Tracker API") as _blocks:
    gr.Markdown("# 📈 OFS Tracker API")
    gr.Markdown(
        "The FastAPI backend is running behind this Gradio Space.\n\n"
        "**API Endpoints:**\n"
        "- `GET /api/issues` — list all tracked OFS issues\n"
        "- `GET /health` — health check\n"
        "- `GET /docs` — interactive API documentation"
    )

# ── Build ASGI app via App.create_app (does NOT start a server or bind ports) ─
# Unlike gr.mount_gradio_app, this only creates the ASGI route tree.
app = GradioApp.create_app(_blocks)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom API routes
app.include_router(router.api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/health")
def api_health_check():
    return {"status": "ok"}

@app.get("/api/status")
def api_status():
    return {"message": "OFS Tracker API is running"}

# ── Startup / shutdown hooks ──────────────────────────────────────────────────
@app.on_event("startup")
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

@app.on_event("shutdown")
async def _shutdown():
    try:
        shutdown_scheduler()
    except Exception as e:
        logger.error(f"Scheduler shutdown failed: {e}")

# ── Local dev entry point ─────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
