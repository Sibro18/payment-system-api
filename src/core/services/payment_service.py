from uuid import UUID
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.core.repositories.account import IAccountRepository
from src.core.repositories.payment import IPaymentRepository
from src.core.repositories.user import IUserRepository

from src.core.dtos.payment import WebhookPayment, PaymentResponse
from src.core.models import Account

class PaymentService:
	INVALID_SIGNATURE = "Invalid signature"
	USER_NOT_FOUND = "User not found"
	ACCOUNT_NOT_BELONG = "Account does not belong to this user"
	TRANSACTION_REPEAT = "Transaction already processed"

	def __init__(
		self,
		user_repo: IUserRepository,
		account_repo: IAccountRepository,
		payment_repo: IPaymentRepository,
		session_factory: async_sessionmaker,
	):
		self.session_factory = session_factory
		self.user_repo = user_repo
		self.account_repo = account_repo
		self.payment_repo = payment_repo


	async def process_webhook(self, dto: WebhookPayment) -> PaymentResponse:
		"""
		Webhook processing in one transaction:
		1. Signature verification
		2. Checking/creating an account
		3. Verifying the uniqueness of the transaction
		4. Creating a payment
		5. Accrual of the amount
		"""

		if not dto.verify_signature():
			raise ValueError(PaymentService.INVALID_SIGNATURE)

		async with self.session_factory() as session:
			async with session.begin():
				user = await self.user_repo.get_by_id(session, dto.user_id)
				if not user:
					raise ValueError(PaymentService.USER_NOT_FOUND)

				account = await self._get_account_or_error(session, dto.account_id, dto.user_id)
				
				existing = await self.payment_repo.get_by_transaction_id(session, dto.transaction_id)
				if existing:
					raise ValueError(PaymentService.TRANSACTION_REPEAT)

				payment = await self.payment_repo.create(
					session,
					dto.to_payment_dict()
				)

				account.balance += dto.amount
				await self.account_repo.update(session, account)
			return PaymentResponse.model_validate(payment)

	async def get_user_payments(self, user_id: UUID):
		async with self.session_factory() as session:
			payments = await self.payment_repo.get_list(session, user_id)
			
			return [PaymentResponse.model_validate(p) for p in payments]
		
	async def _get_account_or_error(self, session: AsyncSession, account_id: UUID, user_id: UUID) -> Account:
		account = await self.account_repo.get_by_id(session, account_id)

		if account and account.user_id != user_id: 
			raise ValueError(PaymentService.ACCOUNT_NOT_BELONG)
		
		if not account:
			account = await self.account_repo.create(
				session, 
				{
					"id": account_id,
					"user_id": user_id,
					"balance": 0
				}
			)
		return account
