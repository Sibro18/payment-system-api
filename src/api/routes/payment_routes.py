from sanic import Blueprint, Request
from sanic.response import json

from src.core.services import PaymentService
from src.core.dtos.payment import WebhookPayment

from ..decorators import auth_required


payment_bp = Blueprint("payment", url_prefix="/payment")

@payment_bp.get("/me")
@auth_required
async def get_me(request: Request):
	payment_service: PaymentService = request.app.ctx.payment_service
	user_id = request.ctx.user_id
	
	response = await payment_service.get_user_payments(user_id)

	return json([p.model_dump(mode="json") for p in response])

@payment_bp.post("/webhook")
async def process_webhook(request: Request):
	payment_service: PaymentService = request.app.ctx.payment_service
	dto = WebhookPayment(**request.json)
	
	response = await payment_service.process_webhook(dto)

	return json(response.model_dump(mode="json"))
