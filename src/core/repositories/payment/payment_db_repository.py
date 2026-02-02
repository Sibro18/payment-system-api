from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .i_payment_repository import IPaymentRepository
from src.core.models import Payment


class PaymentDbRepository(IPaymentRepository):
	def __init__(self):
		pass

	async def get_list(self, session: AsyncSession, user_id: UUID) -> List[Payment]:
		statement = select(Payment).where(Payment.user_id == user_id)

		return list(await session.scalars(statement))

	async def get_by_transaction_id(self, session: AsyncSession, transaction_id: UUID) -> Payment:
		statement = select(Payment).where(Payment.transaction_id == transaction_id)

		return await session.scalar(statement)
	
	async def create(self, session: AsyncSession, data: dict) -> Payment:
		account = Payment(**data)
		
		session.add(account)
		await session.flush()

		return account
