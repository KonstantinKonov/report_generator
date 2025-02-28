from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload
from pydantic import EmailStr

from src.repository.base_repo import BaseRepo
from src.models.reports import ReportsOrm


class ReportsRepo(BaseRepo):
    model = ReportsOrm 
    #mapper = ReportsDataMapper