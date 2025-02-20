from fastapi import APIRouter, Response

from src.schemas import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import UserEmailAlreadyExistsHTTPException, IncorrectPasswordHTTPException


router = APIRouter(prefix="/auth", tags=["Authorization and authentication", ])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep
):
    try:
        await AuthService(db).register_user(data)
    except UserEmailAlreadyExistsHTTPException:
        raise UserEmailAlreadyExistsHTTPException

    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
    db: DBDep
):
    try:
        access_token = await AuthService(db).login_user(data)
    except UserEmailAlreadyExistsHTTPException:
        raise UserEmailAlreadyExistsHTTPException
    except IncorrectPasswordHTTPException:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(
    response: Response
):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get("/me")
async def get_me(
    user_id: UserIdDep,
    db: DBDep
):
    return await AuthService(db).get_one_or_none_user(user_id)