from app.api.endpoints import posts
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])


@api_router.get("/ping")
async def ping():
    return {"message": "pong"}
