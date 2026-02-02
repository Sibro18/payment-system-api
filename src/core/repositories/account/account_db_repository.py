from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .i_account_repository import IAccountRepository
from src.core.models import Account


class AccountDbRepository(IAccountRepository):
	def __init__(self): 
		pass

	async def get_by_id(self, session: AsyncSession, account_id: UUID) -> Optional[Account]:
		return await session.get(Account, account_id)
	
	async def get_list(self, session: AsyncSession, user_id: UUID) -> List[Account]:
		statement = select(Account).where(Account.user_id == user_id)
		
		return list(await session.scalars(statement))

	async def create(self, session: AsyncSession, data: dict) -> Account:
		account = Account(**data)
		
		session.add(account)
		await session.flush()

		return account

	async def update(self, session: AsyncSession, account: Account) -> Account:
		await session.flush()
		
		return account
