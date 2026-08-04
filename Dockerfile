# Stage 1: Build the Next.js frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./

# Pass the API URL as a build arg so the static export knows where to point.
# Since the backend serves the frontend, they share the same origin, so /api is sufficient.
ARG NEXT_PUBLIC_API_URL=/api
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

RUN npm run build

# Stage 2: Build the FastAPI backend and final image
FROM python:3.12-slim
WORKDIR /opt/app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./

# Copy the statically exported frontend files from Stage 1
COPY --from=frontend-builder /app/frontend/out ./frontend/out

# Ensure the SQLite data directory exists
RUN mkdir -p /app/data

# Run the FastAPI server
CMD ["python", "run.py"]
