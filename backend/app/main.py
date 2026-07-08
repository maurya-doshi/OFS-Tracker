import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.api import router

# Ensure the data directory exists for SQLite
os.makedirs("/app/data", exist_ok=True)

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    from app.scheduler import start_scheduler, shutdown_scheduler
    start_scheduler()
    yield
    # Shutdown
    shutdown_scheduler()

app = FastAPI(title="OFS Live Bid Tracker API", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "OFS Tracker API is running"}
