from sanic import Sanic
from sanic_ext import Extend
from sanic.response import json

from src.core.repositories.user import UserDbRepository
from src.core.repositories.account import AccountDbRepository
from src.core.repositories.payment import PaymentDbRepository

from src.core.services import UserService
from src.core.services import AccountService
from src.core.services import PaymentService

from src.database import init_db, async_session_factory, engine

from src.api.routes.user_routes import user_bp
from src.api.routes.auth_routes import auth_bp
from src.api.routes.account_routes import account_bp
from src.api.routes.payment_routes import payment_bp


APP_NAME = "PaymentSystemApi"
HOST = "0.0.0.0"
PORT = 8000

app = Sanic(APP_NAME)

Extend(app)


app.blueprint(auth_bp)
app.blueprint(user_bp)
app.blueprint(account_bp)
app.blueprint(payment_bp)

@app.before_server_start
async def setup_services(app):
	ctx = app.ctx

	ctx.user_repo = UserDbRepository()
	ctx.account_repo = AccountDbRepository()
	ctx.payment_repo = PaymentDbRepository()

	ctx.user_service = UserService(
		ctx.user_repo,
		async_session_factory,
	)

	ctx.account_service = AccountService(
		ctx.account_repo,
		async_session_factory
	)

	ctx.payment_service = PaymentService(
		ctx.user_repo,
		ctx.account_repo,
		ctx.payment_repo,
		async_session_factory
	)

init_db(app)

@app.exception(Exception) 
async def handle_exceptions(request, exception): 
	return json({"error": str(exception)}, status=400)

@app.before_server_stop
async def cleanup_db_connections(app):
	print("Closing database connections...")
	await engine.dispose()
	print("Database connections closed")


if __name__ == "__main__":
	app.run(host=HOST, port=PORT, auto_reload=True, workers=1)
