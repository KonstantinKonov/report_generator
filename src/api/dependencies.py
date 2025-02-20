from typing import Annotated

from fastapi import Depends, Request

from src.utils.db_manager import DBManager
from src.database import ASession
from src.services import AuthService
from src.exceptions import NoAccessTokenHTTPException, \
    IncorrectTokenHTTPException



# database dependency
async def get_db():
    async with DBManager(sessionmaker=ASession) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


# user dependency
def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise NoAccessTokenHTTPException
    return token

def get_current_user_id(token: str = Depends(get_token)):
    try:
        data = AuthService().decode_token(token)
    except IncorrectTokenHTTPException:
        raise IncorrectTokenHTTPException
    return data["user_id"]

 
UserIdDep = Annotated[int, Depends(get_current_user_id)]