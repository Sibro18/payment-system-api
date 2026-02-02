"""add_test_users_and_accounts

Revision ID: 868c85661a18
Revises: 9a3ba15c67f1
Create Date: 2026-02-02 18:10:31.960056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy.dialects import postgresql

import uuid
from datetime import datetime
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# revision identifiers, used by Alembic.
revision: str = '868c85661a18'
down_revision: Union[str, Sequence[str], None] = '9a3ba15c67f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

USER_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")
ADMIN_ID = uuid.UUID("22222222-2222-2222-2222-222222222222")
ACCOUNT_ID = uuid.UUID("33333333-3333-3333-3333-333333333333")

def get_user():
	return {
		"id": USER_ID,
		"email": "user@example.com",
		"full_name": "User",
		"password": pwd_context.hash("1234567890"),
		"is_admin": False,
        "created_at": datetime.now(),
        "updated_at": None
	}

def get_user_account():
	return {
		"id": ACCOUNT_ID,
		"user_id": USER_ID,
		"balance": 0.00,
        "created_at": datetime.now(),
        "updated_at": None
	}

def get_admin():
	return {
		"id": ADMIN_ID,
		"email": "admin@example.com",
		"full_name": "Admin",
		"password": pwd_context.hash("1234567890"),
		"is_admin": True,
		"created_at": datetime.now(),
		"updated_at": None
	}

def upgrade() -> None:
	"""Upgrade schema."""
	user_table = table('user',
		column('id', postgresql.UUID),
		column('email', sa.String),
		column('full_name', sa.String),
		column('password', sa.String),
		column('is_admin', sa.Boolean),
		column('created_at', sa.DateTime),
		column('updated_at', sa.DateTime)
	)

	account_table = table('account',
		column('id', postgresql.UUID),
		column('user_id', postgresql.UUID),
		column('balance', sa.Numeric),
		column('created_at', sa.DateTime),
		column('updated_at', sa.DateTime)
	)

	user_obj = get_user()
	admin_obj = get_admin()
	account_obj = get_user_account()

	op.bulk_insert(
		user_table, 
		[user_obj, admin_obj]
	)

	op.bulk_insert(
		account_table, 
		[account_obj]
	)

	pass


def downgrade() -> None:
	"""Downgrade schema."""
	op.execute(
		sa.text('DELETE FROM "account" where "id" = :id')
		.bindparams(id=ACCOUNT_ID)
	)
	op.execute(
		sa.text('DELETE FROM "user" WHERE "id" IN (:u, :a)')
		.bindparams(u=USER_ID, a=ADMIN_ID)
	)
