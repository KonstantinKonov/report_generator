from src.services.base import BaseService
from src.utils.db_manager import DBManager
from src.schemas import RoleAdd, RolePatch


class RolesService(BaseService):
    async def get_all_roles(self):
        return await self.db.roles.get_all()

    
    async def add_role(self, data: RoleAdd):
        await self.db.roles.add(data)
        await self.db.commit()


    async def edit_role(self, role_id: int, data: RolePatch):
        await self.db.roles.edit(data, id=role_id)
        await self.db.commit()


    async def delete_role(self, role_id: int):
        await self.db.roles.delete(id=role_id)
        await self.db.commit()
