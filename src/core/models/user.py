from sqlalchemy import Column, UUID, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from src.database import Base


class User(Base):
	__tablename__ = "user"

	id			= Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
	email		= Column(String, unique=True, index=True, nullable=False)
	full_name	= Column(String, nullable=True)
	password	= Column(String, nullable=False)
	is_admin	= Column(Boolean, default=False)
	created_at	= Column(DateTime(timezone=True), server_default=func.now())
	updated_at	= Column(DateTime(timezone=True), onupdate=func.now())

	accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
	payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
