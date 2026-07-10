from fastapi import APIRouter
from backend.app.api import endpoints

api_router = APIRouter()
api_router.include_router(endpoints.router)
