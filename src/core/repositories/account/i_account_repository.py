from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Account


class IAccountRepository(ABC):
	@abstractmethod
	async def get_by_id(self, session: AsyncSession, account_id: UUID) -> Optional[Account]:
		pass

	@abstractmethod
	async def get_list(self, session: AsyncSession, user_id: UUID) -> List[Account]:
		pass

	@abstractmethod
	async def create(self, session: AsyncSession, data: dict) -> Account:
		pass

	@abstractmethod
	async def update(self, session: AsyncSession, account: Account) -> Account:
		pass