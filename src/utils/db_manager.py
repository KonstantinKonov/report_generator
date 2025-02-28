from src.repository import UsersRepo, ReportsRepo, RolesRepo


class DBManager:
    def __init__(self, sessionmaker):
        self.sessionmaker = sessionmaker

    async def __aenter__(self):
        self.session = self.sessionmaker()

        self.users = UsersRepo(self.session)
        self.reports = ReportsRepo(self.session)
        self.roles = RolesRepo(self.session)

        return self


    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()


    async def commit(self):
        await self.session.commit()