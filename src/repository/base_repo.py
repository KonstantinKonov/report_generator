from typing import Sequence

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from asyncpg.exceptions import UniqueViolationError

from src.database import Base
from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException


class BaseRepo:
    model: Base
    sesson: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_one_or_none(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def get_one_or_raise(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        res = await self.session.execute(query)
        if res is None:
            raise ObjectNotFoundException # сюда ничего не передаем?
        return res

    async def add(self, data: BaseModel):
        try:
            stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            res = await self.session.execute(stmt)
            model = res.scalar_one()
            return model
        except IntegrityError as e:
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from e

    async def add_bulk(self, data: Sequence[BaseModel]):
        try:
            stmt = insert(self.model).values([item.model_dump() for item in data])
            await self.session.execute(stmt)
        except IntegrityError as e:
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from e

    async def edit(self, data: Sequence[BaseModel], **filter_by):
        try:
            stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=True)) # возврат значения при edit с помощью returning
            await self.session.execute(stmt)
        except IntegrityError as e:
            raise e

    async def delete(self, **filter_by):
        try:
            stmt = delete(self.model).filter_by(**filter_by)
            await self.session.execute(stmt)
        except IntegrityError as e:
            raise e
