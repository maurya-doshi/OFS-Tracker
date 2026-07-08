import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.api import router

# Ensure the data directory exists for SQLite
os.makedirs("data", exist_ok=True)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="OFS Live Bid Tracker API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.api_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    # Initialize scheduler here
    from app.scheduler import start_scheduler
    start_scheduler()

@app.get("/")
def root():
    return {"message": "OFS Tracker API is running"}
