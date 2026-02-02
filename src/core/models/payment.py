from sqlalchemy import Column, UUID, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from src.database import Base


class Payment(Base):
	__tablename__ = "payment"
	
	id				= Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
	transaction_id	= Column(UUID(as_uuid=True), unique=True, nullable=False)
	user_id			= Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
	account_id		= Column(UUID(as_uuid=True), ForeignKey("account.id", ondelete="CASCADE"), nullable=False)
	amount			= Column(Numeric(10, 2), nullable=False)
	created_at		= Column(DateTime(timezone=True), server_default=func.now())
	
	user	= relationship("User", back_populates="payments")
	account = relationship("Account", back_populates="payments")
