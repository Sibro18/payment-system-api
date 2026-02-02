from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import Config


class Base(DeclarativeBase):
	pass

engine = create_async_engine(Config.DATABASE_URL, echo=True)

async_session_factory = async_sessionmaker(
	engine, class_=AsyncSession, expire_on_commit=False
)

def init_db(app) -> async_sessionmaker:
	@app.listener('before_server_start')
	async def setup_db(app, loop):
		async with engine.begin() as conn:
			await conn.run_sync(Base.metadata.create_all)
	return async_session_factory