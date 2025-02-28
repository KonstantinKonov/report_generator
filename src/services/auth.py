from datetime import datetime, timezone, timedelta

import os
import jwt
import hashlib
import base64

from src.config import settings
from src.services.base import BaseService
from src.schemas import UserRequestAdd, UserAdd, UserWithRoleRequestAdd
from src.exceptions import UserAlreadyExistsException, \
    IncorrectTokenHTTPException, \
    ObjectAlreadyExistsException, \
    EmailNotRegisteredHTTPException, \
    IncorrectPasswordHTTPException


class AuthService(BaseService):

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        print(f'data to encode {to_encode}')
        encoded_jwt = jwt.encode(
            to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    
    def hash_password(self, password: str) -> str:
        salted_password = base64.b64decode(settings.HASH_SALT) + password.encode('utf-8')
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        return hashed_password

    
    def verify_password(self, password, stored_hashed_password) -> bool:
        hashed_password = self.hash_password(password)
        return hashed_password == stored_hashed_password

    
    def decode_token(self, token: str) -> dict:
        try:
            res = jwt.decode(token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return res
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenHTTPException


    async def register_user(self, data: UserWithRoleRequestAdd):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password, role_id=data.role_id)
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex


    async def login_user(self, data: UserRequestAdd):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        print(user)
        if user is None:
            raise EmailNotRegisteredHTTPException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordHTTPException
        access_token = self.create_access_token({"user_id": user.id, "role": user.role.role})
        return access_token


    async def get_one_or_none_user(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)