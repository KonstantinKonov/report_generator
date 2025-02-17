from src.repository import UsersRepository


class DBManager:
    def __init__(self, sessionmaker):
        self.sessionmaker = sessionmaker

    async def __aenter__(self):
        self.session = self.sessionmaker()

        self.users = UsersRepository(self.session)

        return self


    async def __aexit__(self):
        await self.session.rollback()
        await self.session.close()


    async def commit(self):
        await self.session.commit()