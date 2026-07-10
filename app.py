import sys
import os

# Ensure the backend directory is in the Python path so absolute imports work
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

import gradio as gr
from api_app.main import app as fastapi_app

# Named `_blocks` (not `demo`) so HF's Gradio runner does NOT auto-launch it
# separately via demo.launch(). Only `app` below is exposed for HF to detect.
_blocks = gr.Blocks(title="OFS Tracker API")
with _blocks:
    gr.Markdown("# 📈 OFS Tracker API")
    gr.Markdown(
        "The FastAPI backend is running behind this Gradio Space.\n\n"
        "**API Endpoints:**\n"
        "- `GET /api/issues` — list all tracked OFS issues\n"
        "- `GET /health` — health check\n"
        "- `GET /docs` — interactive API documentation"
    )

# Mount Gradio at / within the FastAPI ASGI app.
# HF detects `app` as an ASGI variable and runs it directly with uvicorn —
# no separate demo.launch() call is made, so there is no port conflict.
app = gr.mount_gradio_app(fastapi_app, _blocks, path="/")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
