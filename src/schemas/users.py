from enum import Enum
from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr


class RoleAdd(BaseModel):
    role: str


class RolePatch(BaseModel):
    role: str | None = None


class Role(RoleAdd):
    id: int


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UserRequestPatch(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


class UserWithRoleRequestAdd(UserRequestAdd):
    role_id: int


class UserWithRoleRequestPatch(UserRequestPatch):
    role_id: int | None = None


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    role_id: int


class User(BaseModel):
    id: int
    email: EmailStr
    role: Role

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str