from fastapi import APIRouter

from app.api.v1 import activities, auth, users

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(users.sport_tags_router)
api_router.include_router(activities.router)


@api_router.get("/ping")
async def ping() -> dict:
    return {"message": "pong"}
