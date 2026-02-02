from sanic import Blueprint, Request
from sanic.response import json
from uuid import UUID

from src.core.dtos.user import UserCreate, UserUpdate
from src.core.services.user_service import UserService

from ..decorators import auth_required, admin_required

user_bp = Blueprint("user", url_prefix="/user")

@user_bp.get("/me")
@auth_required
async def get_me(request: Request):
	user_service: UserService = request.app.ctx.user_service

	user_id = request.ctx.user_id
	user = await user_service.get_user(user_id)

	return json(user.model_dump(mode="json"))


@user_bp.get("/list")
@admin_required
async def get_users(request: Request):
	user_service: UserService = request.app.ctx.user_service

	if not request.ctx.is_admin:
		return json({"error": "Forbidden"}, status=403)

	users = await user_service.get_users()
	
	return json([u.model_dump(mode="json") for u in users])


@user_bp.post("/")
@admin_required
async def admin_create_user(request: Request):

	if not request.ctx.is_admin:
		return json({"error": "Forbidden"}, status=403)

	user_service: UserService = request.app.ctx.user_service

	dto = UserCreate(**request.json)
	user = await user_service.create_user(dto)

	return json(user.model_dump(mode="json"))


@user_bp.put("/<user_id:uuid>")
@admin_required
async def admin_update_user(request: Request, user_id: UUID):
	if not request.ctx.is_admin:
		return json({"error": "Forbidden"}, status=403)

	if not user_id: 
		return json({"error": "Missing id"}, status=400)
	
	user_service: UserService = request.app.ctx.user_service

	dto = UserUpdate(**request.json)
	user = await user_service.update_user(user_id, dto)

	return json(user.model_dump(mode="json"))


@user_bp.delete("/<user_id:uuid>")
@admin_required
async def admin_delete_user(request: Request, user_id: UUID):
	if not request.ctx.is_admin:
		return json({"error": "Forbidden"}, status=403)

	if not user_id: 
		return json({"error": "Missing id"}, status=400)

	user_service: UserService = request.app.ctx.user_service
	await user_service.delete_user(user_id)

	return json({"status": "deleted"})
