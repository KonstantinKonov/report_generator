from fastapi import APIRouter, HTTPException, Response

from src.schemas import UserRequestAdd, UserAdd
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Authorization and authentication", ])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep
)
    ...