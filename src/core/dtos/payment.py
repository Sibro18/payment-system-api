from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
import hashlib
from uuid import UUID
from decimal import Decimal

from src.config import Config


class WebhookPayment(BaseModel):
	transaction_id: UUID
	user_id: 		UUID
	account_id: 	UUID
	amount: 		Decimal
	signature: 		str

	@field_validator('amount')
	def amount_positive(cls, v):
		if v <= 0:
			raise ValueError('Amount must be positive')
		
		return v

	def verify_signature(self) -> bool:
		data_string = f"{self.account_id}{self.amount}{self.transaction_id}{self.user_id}{Config.SECRET_KEY_WEBHOOK}"
		expected_signature = hashlib.sha256(data_string.encode()).hexdigest()

		return self.signature == expected_signature

	def to_payment_dict(self):
		return {
			"transaction_id": self.transaction_id,
			"user_id": self.user_id,
			"account_id": self.account_id,
			"amount": self.amount
		}

class PaymentResponse(BaseModel):
	id: 			UUID
	transaction_id: UUID
	user_id: 		UUID
	account_id: 	UUID
	amount: 		Decimal
	created_at: 	datetime

	model_config = ConfigDict(from_attributes=True)
