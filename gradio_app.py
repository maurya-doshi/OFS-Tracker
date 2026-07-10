import gradio as gr
from backend.app.main import app as fastapi_app

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
