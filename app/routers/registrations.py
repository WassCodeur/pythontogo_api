from app.database.orm import select
from app.utils.registrations import (
    create_registration,
)
from app.utils.tickets import get_ticket_by_id
import httpx
from uuid import uuid4

from app.schemas.models import (
    MessageResponse,
    RegistrationCreate,
    RegistrationSummary,
    RegistrationUpdate
)
from app.core.settings import logger, settings
from fastapi import APIRouter, Depends, HTTPException, Request, status, BackgroundTasks


from app.database.connection import get_db_connection


api_router = APIRouter(tags=["registrations"])
base_url = settings.base_url.rstrip("/")
base_url = f"{base_url}/{settings.root_path.strip('/')}" if settings.root_path else base_url


@api_router.post("/register/{event_code}", status_code=status.HTTP_201_CREATED)
async def register_for_event(request: Request, registration: RegistrationCreate, event_code: str, background_tasks: BackgroundTasks, db=Depends(get_db_connection)):
    """
    Register a user for an event.
    """
    try:
        auth = request.headers.get("Authorization")
        event_existing = await select(db, "events", filter={"code": event_code.upper()})
        if not event_existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        if not auth or not auth.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        ticket = await get_ticket_by_id(db, registration.ticket_id)
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
        if ticket['quantity'] < 1 or ticket['quantity'] < registration.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Not enough slots available for the selected ticket. Available quantity: {ticket['quantity']}")

        registration_id = uuid4()
        registration_data = {
            "id": str(registration_id),
            "event_id": event_existing[0]["id"],
            "full_name": registration.full_name,
            "email": registration.email,
            "whatsapp_number": registration.whatsapp_number,
            "ticket_type": registration.ticket_type,
            "ticket_id": registration.ticket_id,
            "ticket_price": registration.ticket_price,
            "ticket_quantity": registration.quantity,
            "attendance_status": registration.attendance_status,
            "payment_status": registration.payment_status,
            "dietary_restrictions": registration.dietary_restrictions,
            "payment_reference": registration.payment_reference,
            "payment_link": registration.payment_link,
            "agreed_to_code_of_conduct": registration.agreed_to_code_of_conduct,
            "agreed_to_privacy_policy": registration.agreed_to_privacy_policy,
            "shared_with_sponsors": registration.shared_with_sponsors
        }
        payment_data = {
            "amount": registration.ticket_price * registration.quantity,
            "callback_url": f"{base_url}/webhooks/paydunya/callback",
            "description": f"Registration for {event_code.upper()} - {registration.full_name}",
            "unit_price": registration.ticket_price,
            "quantity": registration.quantity,
            "name": registration.ticket_type,
            "success_page_url": (registration.success_page_url and registration.success_page_url.startswith("http")) or f"{base_url}/checkout/payment-success",
            "cancel_page_url": (registration.cancel_page_url and registration.cancel_page_url.startswith("http")) or f"{base_url}/checkout/payment-cancel"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{base_url}/checkout/payment", headers={"Authorization": auth}, json=payment_data)
            response.raise_for_status()
            result = response.json()
            payment_token = result.get("payment_url").split(
                "/")[-1]  # Extract token from URL
            registration_data["payment_reference"] = payment_token
            registration_data["payment_link"] = result.get("payment_url")

            background_tasks.add_task(
                create_registration, db, registration_data)

            return result
    except Exception as e:
        logger.error(f"Error creating registration: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")
