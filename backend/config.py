import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////app/data/ofs_tracker.db")
