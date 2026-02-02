from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Payment


class IPaymentRepository(ABC):
	@abstractmethod
	async def get_list(self, session: AsyncSession, user_id: UUID) -> List[Payment]:
		pass

	@abstractmethod
	async def get_by_transaction_id(self, session: AsyncSession, transaction_id: UUID) -> Payment:
		pass

	@abstractmethod
	async def create(self, session: AsyncSession, data: dict) -> Payment:
		pass
