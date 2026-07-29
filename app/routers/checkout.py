from fastapi import APIRouter, Request, HTTPException, status
from app.core.settings import settings, logger
from app.schemas.payment import Payment
from app.payments.paydunya_service import create_invoice


api_router = APIRouter(prefix="/checkout", tags=["checkout"])
base_url = settings.base_url.rstrip("/")
root_path = settings.root_path.rstrip("/").lstrip("/")
base_url = f"{base_url}/{root_path}" if root_path else base_url


@api_router.post("/payment")
def create_payment(payment: Payment):
    try:
        # webhook_url = f"{base_url}/webhooks/paydunya/callback"
        url = create_invoice(
            description=payment.description,
            # callback_url=webhook_url,
            unit_price=payment.unit_price,
            qte=payment.quantity,
            name=payment.name,
            success_page_url=payment.success_page_url,
            cancel_page_url=payment.cancel_page_url
        )

        return url
    except Exception as e:
        logger.error(f"Error creating payment: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="failed to process payment")
