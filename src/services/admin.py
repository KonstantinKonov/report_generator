from src.services.base import BaseService
from src.utils.db_manager import DBManager
from src.schemas import UserWithRoleRequestAdd, UserAdd
from src.services import AuthService

class AdminService(BaseService):
    async def get_all_users(self):
        return await self.db.users.get_all()

    async def add_user(self, data: UserWithRoleRequestAdd):
        ...

    async def get_one_or_none(self, user_id):
        return await self.db.users.get_one_or_none(id=user_id)


    async def edit_user(self, user_id: int, data: UserWithRoleRequestAdd):
        await self.db.users.edit(data, id=user_id)
        await self.db.commit()

    async def delete_user(self, user_id: int):
        await self.db.users.delete(id=user_id)
        await self.db.commit()