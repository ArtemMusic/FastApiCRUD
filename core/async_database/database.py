from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session


class Database:
    def __init__(self, url: str):
        self.engine = create_async_engine(url)

        self.session_factory = async_sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False
        )

    async def scoped_session_dependency(self) -> AsyncSession:
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        yield session
        await session.close()


database = Database(f"sqlite+aiosqlite:///./sqliteASYNC.db")
