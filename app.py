import sys
import os

# ── Ensure backend/ is on the Python path ─────────────────────────────────────
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import the FastAPI app (api_app.main handles DATABASE_URL setup at module level)
from api_app.main import app as fastapi_app

import gradio as gr

# ── Minimal Gradio UI ─────────────────────────────────────────────────────────
with gr.Blocks(title="OFS Tracker API") as _blocks:
    gr.Markdown("# 📈 OFS Tracker API")
    gr.Markdown(
        "The FastAPI backend is running behind this Gradio Space.\n\n"
        "**API Endpoints:**\n"
        "- `GET /api/issues` — list all tracked OFS issues\n"
        "- `GET /health` — health check\n"
        "- `GET /docs` — interactive API documentation"
    )

# ── Mount Gradio onto the FastAPI app ─────────────────────────────────────────
# mount_gradio_app properly initialises Gradio's queue (unlike App.create_app).
# HF Spaces detects the `app` ASGI variable and serves it with their own uvicorn
# on port 7860 — we do NOT start uvicorn ourselves to avoid double-binding.
app = gr.mount_gradio_app(fastapi_app, _blocks, path="/")
