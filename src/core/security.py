import jwt
from datetime import datetime, timedelta, timezone

from src.config import Config


def create_access_token(data: dict) -> str:
	to_encode = data.copy()
	expire = datetime.now(timezone.utc) + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})

	encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

	return encoded_jwt

def verify_access_token(token: str) -> dict:
	TOKEN_EXPIRED = "Token has expired"
	INVALID_TOKEN = "Invalid token"

	try:
		payload = jwt.decode(
			token,
			Config.SECRET_KEY,
			algorithms=[Config.JWT_ALGORITHM]
		)
		
		return payload
	except jwt.ExpiredSignatureError:
		raise ValueError(TOKEN_EXPIRED)
	except jwt.InvalidTokenError:
		raise ValueError(INVALID_TOKEN)
