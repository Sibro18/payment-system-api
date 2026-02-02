from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import User


class IUserRepository(ABC):
	@abstractmethod
	async def get_by_id(self, session: AsyncSession, user_id: UUID) -> Optional[User]:
		pass

	@abstractmethod
	async def get_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
		pass

	@abstractmethod
	async def get_list(self, session: AsyncSession) -> List[User]:
		pass

	@abstractmethod
	async def create(self, session: AsyncSession, data: dict) -> User:
		pass

	@abstractmethod
	async def delete(self, session: AsyncSession, user_id: UUID) -> None:
		pass
