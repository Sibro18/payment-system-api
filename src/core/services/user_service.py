from uuid import UUID
from passlib.context import CryptContext
from typing import List
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.core.repositories.user import IUserRepository

from src.core.dtos.user import (
    UserCreate, UserUpdate, UserLogin,
    UserResponse, Token, TokenData, AuthResponse,
	UserWithAccountsResponse
)
from src.core.models import User

from src.core.security import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
	INVALID_CREDENTIALS = "Invalid credentials"
	USER_NOT_FOUND = "User not found"
	EMAIL_EXISTS = "User with this email already exists"
	
	PASSWORD_FIELD = "password"
	TOKEN_TYPE = "bearer"
	
	def __init__(
		self,
		user_repo: IUserRepository,
		session_factory: async_sessionmaker
	):
		self.user_repo = user_repo
		self.session_factory = session_factory

	async def authenticate(self, dto: UserLogin) -> AuthResponse:
		async with self.session_factory() as session:
			user = await self.user_repo.get_by_email(session, dto.email)

			if not user:
				raise ValueError(UserService.INVALID_CREDENTIALS)

			if not pwd_context.verify(dto.password, user.password):
				raise ValueError(UserService.INVALID_CREDENTIALS)

			token_data = TokenData(
				user_id=str(user.id),
				is_admin=user.is_admin
			)

			access_token = create_access_token(token_data.model_dump())

			return AuthResponse(
				user=UserResponse.model_validate(user),
				token=Token(
					access_token=access_token, 
					token_type=UserService.TOKEN_TYPE
				)
			)

	async def get_users(self) -> List[UserWithAccountsResponse]:
		async with self.session_factory() as session:
			user_list = await self.user_repo.get_list(session)
			
			return [UserWithAccountsResponse.model_validate(u) for u in user_list] 

	async def get_user(self, user_id: UUID) -> UserResponse:
		async with self.session_factory() as session:
			user = await self._get_user_or_error(session, user_id)

			return UserResponse.model_validate(user)

	async def create_user(self, dto: UserCreate) -> UserResponse:
		async with self.session_factory() as session:
			async with session.begin():
				existing = await self.user_repo.get_by_email(session, dto.email)
				if existing:
					raise ValueError(UserService.EMAIL_EXISTS)

				data = dto.model_dump()
				data[UserService.PASSWORD_FIELD] = self._hash(data.pop(UserService.PASSWORD_FIELD))

				user = await self.user_repo.create(session, data)

			return UserResponse.model_validate(user)

	async def update_user(self, user_id: UUID, dto: UserUpdate) -> UserResponse:
		async with self.session_factory() as session:
			async with session.begin():
				user = await self._get_user_or_error(session, user_id)
				
				data = dto.model_dump(exclude_unset=True)

				if UserService.PASSWORD_FIELD in data:
					data[UserService.PASSWORD_FIELD] = self._hash(data.pop(UserService.PASSWORD_FIELD))

				for key, value in data.items():
					setattr(user, key, value)
			await session.refresh(user)

			return UserResponse.model_validate(user)

	async def delete_user(self, user_id: UUID):
		async with self.session_factory() as session:
			async with session.begin():
				user = await self._get_user_or_error(session, user_id)
				await self.user_repo.delete(session, user)
	
	async def _get_user_or_error(self, session: AsyncSession, id: UUID) -> User:
		user = await self.user_repo.get_by_id(session, id)
		
		if not user:
			raise ValueError(UserService.USER_NOT_FOUND)

		return user
	
	def _hash(self, password: str) -> str:
		return pwd_context.hash(password)