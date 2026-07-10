import sys
import os

# Ensure the backend directory is in the Python path so absolute imports like 'from app...' work
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

import gradio as gr
from api_app.main import app as fastapi_app

# Create a minimal Gradio UI to satisfy Hugging Face's Gradio SDK requirements
demo = gr.Blocks()
with demo:
    gr.Markdown("# OFS Tracker API")
    gr.Markdown("The FastAPI backend is running perfectly behind this Gradio Space.")
    gr.Markdown("API Endpoint: `/api/issues`")

# Mount the FastAPI app. 
# Hugging Face Spaces natively looks for a variable named `app` and will run it with Uvicorn.
# We mount our FastAPI app at the root (/) and the dummy Gradio UI at (/ui)
app = gr.mount_gradio_app(fastapi_app, demo, path="/ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
