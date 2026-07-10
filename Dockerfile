FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the backend requirements and install them
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ .

# Ensure data directory exists and has the right permissions for HuggingFace (runs as user 1000)
RUN mkdir -p /app/data && chmod -R 777 /app/data

# HuggingFace Spaces sets PORT to 7860 by default
ENV PORT=7860
EXPOSE 7860

# Run the app
CMD ["python", "run.py"]
