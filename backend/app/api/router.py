from fastapi import APIRouter
from app.api.endpoints import copy, brand, vision

api_router = APIRouter()
api_router.include_router(copy.router, prefix="/copy", tags=["copy"])
api_router.include_router(brand.router, prefix="/brand", tags=["brand"])
api_router.include_router(vision.router, prefix="/vision", tags=["vision"])
