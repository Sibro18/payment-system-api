from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

class AccountBase(BaseModel):
	balance: float

class AccountResponse(AccountBase):
	id: 		UUID
	user_id: 	UUID
	created_at: datetime
	updated_at: Optional[datetime]

	model_config = ConfigDict(from_attributes=True)
