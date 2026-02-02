from sanic import Blueprint, Request
from sanic.response import json

from src.core.dtos.user import UserLogin
from src.core.services import UserService


auth_bp = Blueprint("auth", url_prefix="/auth")

@auth_bp.post("/")
async def login(request: Request):
	user_service: UserService = request.app.ctx.user_service
	
	dto = UserLogin(**request.json)
	auth_response = await user_service.authenticate(dto)

	return json(auth_response.model_dump(mode="json"))
