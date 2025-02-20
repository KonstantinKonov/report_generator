from sqlalchemy import select, insert, update, delete
from pydantic import EmailStr

from src.repository.base_repo import BaseRepo
from src.models.users import UsersOrm


class UsersRepo(BaseRepo):
    model = UsersOrm
    #mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        res = await self.session.execute(query)
        model = res.scalar_one_or_none()

        return model
        #return UserWithHashedPassword.model_valudate(model)