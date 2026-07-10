import sys
import os

# Ensure the backend directory is in the Python path so absolute imports work
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

import gradio as gr
from api_app.main import app as fastapi_app

# Create a minimal Gradio UI that HF can detect and serve
with gr.Blocks(title="OFS Tracker API") as demo:
    gr.Markdown("# 📈 OFS Tracker API")
    gr.Markdown(
        "The FastAPI backend is running behind this Gradio Space.\n\n"
        "**API Endpoints:**\n"
        "- `GET /api/issues` — list all tracked OFS issues\n"
        "- `GET /health` — health check\n"
        "- `GET /docs` — interactive API documentation"
    )

# Mount the FastAPI app under /backend, and expose the Gradio demo at /
# HF Gradio SDK looks for a top-level `app` ASGI variable or runs `demo.launch()`.
# Using gr.mount_gradio_app makes `app` the combined ASGI app HF will serve.
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
