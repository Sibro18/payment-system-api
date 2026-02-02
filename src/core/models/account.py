from sqlalchemy import Column, UUID, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from src.database import Base


class Account(Base):
	__tablename__ = "account"
	
	id			= Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
	user_id		= Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
	balance		= Column(Numeric(10, 2), default="0")
	created_at	= Column(DateTime(timezone=True), server_default=func.now())
	updated_at	= Column(DateTime(timezone=True), onupdate=func.now())
	
	user		= relationship("User", back_populates="accounts")
	payments 	= relationship("Payment", back_populates="account", cascade="all, delete-orphan")