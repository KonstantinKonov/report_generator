from src.services.base import BaseService
from src.utils.db_manager import DBManager
from src.schemas import Report, ReportAdd 


class ReportService(BaseService): # здесь нужно ли pagination
    async def get_all_reports(self):
        return await self.db.reports.get_all()


    async def add_report(self, data: ReportAdd):
        return await self.db.reports.add_one(data)