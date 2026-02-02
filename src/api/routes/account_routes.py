from sanic import Blueprint, Request
from sanic.response import json

from src.core.services import AccountService

from ..decorators import auth_required


account_bp = Blueprint("account", url_prefix="/account")

@account_bp.get("/me")
@auth_required
async def get_me(request: Request):
	account_service: AccountService = request.app.ctx.account_service
	user_id = request.ctx.user_id
	
	response = await account_service.get_user_accounts(user_id)

	return json([a.model_dump(mode="json") for a in response])
