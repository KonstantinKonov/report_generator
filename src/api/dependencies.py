from typing import Annotated

from fastapi import Depends, Request

from src.utils.db_manager import DBManager
from src.database import ASession
from src.services import AuthService
from src.schemas import User
from src.exceptions import NoAccessTokenHTTPException, \
    IncorrectTokenHTTPException, \
    UnauthorizedHTTPException



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

def get_current_user_role(token: str = Depends(get_token)):
    try:
        data = AuthService().decode_token(token)
    except IncorrectTokenHTTPException:
        raise IncorrectTokenHTTPException
    return data["role"]
    

def get_current_user_id(token: str = Depends(get_token)):
    try:
        data = AuthService().decode_token(token)
    except IncorrectTokenHTTPException:
        raise IncorrectTokenHTTPException
    return data["user_id"]

 
UserIdDep = Annotated[int, Depends(get_current_user_id)]


# roles dependency
'''
def check_roles(required_roles: list, token: str = Depends(get_token)):
    try:
        data = AuthService().decode_token(token)
        if data.role in required_roles:
            return True
    except IncorrectTokenHTTPException:
        raise IncorrectTokenHTTPException
    except UnauthorizedHTTPException:
        raise UnauthorizedHTTPException
'''


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, role: Annotated[User, Depends(get_current_user_role)]):
        if role in self.allowed_roles:
            return True
        raise UnauthorizedHTTPException


RolesAdminDep = Annotated[bool, Depends(RoleChecker(allowed_roles=["admin", ]))]
RolesUserDep = Annotated[bool, Depends(RoleChecker(allowed_roles=["user", ]))]
RolesAnalyticDep = Annotated[bool, Depends(RoleChecker(allowed_roles=["analytic", ]))]
RolesHeadAnalyticDep = Annotated[bool, Depends(RoleChecker(allowed_roles=["head_analytic"]))]
RolesAllDep = Annotated[bool, Depends(RoleChecker(allowed_roles=["admin", "user", "analytic", "head_analytic"]))]