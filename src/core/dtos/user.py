from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from .account import AccountResponse


class UserBase(BaseModel):
	email: 		EmailStr
	full_name: 	Optional[str]
	is_admin: 	bool

class UserCreate(UserBase):
	password: str

	@field_validator('password')
	def password_length(cls, v):
		if len(v) < 8:
			raise ValueError('Password must be at least 8 characters long')
		
		return v

class UserUpdate(BaseModel):
	email:		Optional[EmailStr]	= None
	full_name:	Optional[str]		= None
	password:	Optional[str]		= None
	is_admin:	Optional[bool]		= None

class UserLogin(BaseModel):
	email:		EmailStr
	password:	str

class UserResponse(UserBase):
	id: 		UUID
	created_at: datetime
	updated_at: Optional[datetime]

	model_config = ConfigDict(from_attributes=True)

class UserWithAccountsResponse(UserResponse):
	accounts: List[AccountResponse]
	
class Token(BaseModel):
	access_token: 	str
	token_type: 	str

class TokenData(BaseModel):
	user_id: 	str
	is_admin: 	bool

class AuthResponse(BaseModel): 
	user: 	UserResponse 
	token: 	Token
