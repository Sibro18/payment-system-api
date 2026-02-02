from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from .i_user_repository import IUserRepository
from src.core.models import User


class UserDbRepository(IUserRepository):
	def __init__(self): 
		pass

	async def get_by_id(self, session: AsyncSession, user_id: UUID) -> Optional[User]:
		return await session.get(User, user_id)

	async def get_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
		statement = select(User).where(User.email == email)
		
		return await session.scalar(statement)
	
	async def get_list(self, session: AsyncSession) -> List[User]:
		statement = select(User).options(selectinload(User.accounts))
		
		return list(await session.scalars(statement))

	async def create(self, session: AsyncSession, data: dict) -> User:
		user = User(**data)
		
		session.add(user)
		await session.flush()

		return user

	async def delete(self, session: AsyncSession, user: User) -> None:
		await session.delete(user)
		await session.flush()
