from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload
from pydantic import EmailStr

from src.repository.base_repo import BaseRepo
from src.models.users import UsersOrm


class UsersRepo(BaseRepo):
    model = UsersOrm
    #mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).options(joinedload(self.model.role)).filter_by(email=email)
        print(query)
        res = await self.session.execute(query)
        print(res)
        model = res.scalar_one_or_none()
        print(model)

        return model
        #return UserWithHashedPassword.model_valudate(model)
