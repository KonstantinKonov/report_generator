from fastapi import APIRouter, Response, Depends

from src.schemas import UserRequestAdd, UserWithRoleRequestAdd, UserAdd, User
from src.services.auth import AuthService
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import UserEmailAlreadyExistsHTTPException, IncorrectPasswordHTTPException


router = APIRouter(prefix="/auth", tags=["Authorization and authentication", ])


@router.post("/register")
async def register_user(
    data: UserWithRoleRequestAdd,
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
): #-> User: нужно для отфильтровывания hashed_password, на каком уровне необходимо фильтровать - в endpoints или на сервисном уровне?
    res = await AuthService(db).get_one_or_none_user(user_id)
    return res # как исключить поле hashed_password