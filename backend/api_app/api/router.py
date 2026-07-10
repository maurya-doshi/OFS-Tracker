from fastapi import APIRouter
from api_app.api import endpoints

api_router = APIRouter()
api_router.include_router(endpoints.router)
