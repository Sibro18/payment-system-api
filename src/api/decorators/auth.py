from functools import wraps
from sanic.exceptions import Unauthorized
from uuid import UUID

from src.core.security import verify_access_token


AUTHORIZATION_HEADER = "Authorization" 
MISSING_TOKEN = "Missing token"
INVALID_TOKEN = "Invalid token"
ADMIN_REQUIRED = "Admin privileges required"

USER_ID = "user_id"
IS_ADMIN = "is_admin"
TOKEN_TYPE = "Bearer"


async def _check_auth(request):
	auth_header = request.headers.get(AUTHORIZATION_HEADER)

	if not auth_header or not auth_header.startswith(f"{TOKEN_TYPE} "):
		raise Unauthorized(MISSING_TOKEN)

	parts = auth_header.split() 
	if len(parts) != 2: 
		raise Unauthorized(INVALID_TOKEN)
	
	token = parts[1]
	payload = verify_access_token(token)

	if not payload:
		raise Unauthorized(INVALID_TOKEN)

	try: 
		request.ctx.user_id = UUID(payload[USER_ID]) 
		request.ctx.is_admin = payload[IS_ADMIN]
	except Exception: 
		raise Unauthorized(INVALID_TOKEN)
	
	# user exists check 
	# NOTE: in production will use refresh-tokens or blacklist
	try:
		user_service = request.app.ctx.user_service 
		await user_service.get_user(payload[USER_ID]) 
	except ValueError:
		raise Unauthorized(INVALID_TOKEN)

def auth_required(f):
	@wraps(f)
	async def decorated(request, *args, **kwargs):
		await _check_auth(request)
		
		return await f(request, *args, **kwargs)
	return decorated

def admin_required(f):
	@wraps(f)
	async def decorated(request, *args, **kwargs):
		await _check_auth(request)
		
		if not request.ctx.is_admin:
			raise Unauthorized(ADMIN_REQUIRED)
		
		return await f(request, *args, **kwargs)
	return decorated
