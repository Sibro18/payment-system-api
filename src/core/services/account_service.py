from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.core.repositories.account import IAccountRepository
from src.core.dtos.account import AccountResponse


class AccountService:
	def __init__(
		self,
		account_repo: IAccountRepository,
		session_factory: async_sessionmaker
	):
		self.session_factory = session_factory
		self.account_repo = account_repo

	async def get_user_accounts(self, user_id: UUID) -> List[AccountResponse]:
		async with self.session_factory() as session:
			accounts = await self.account_repo.get_list(session, user_id)
			
			return [AccountResponse.model_validate(a) for a in accounts]
