from typing import Annotated

from fastapi import Depends

from src.utils.db_manager import DBManager
from src.database import ASession


async def get_db():
    async with DBManager(sessionmaker=ASession) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]