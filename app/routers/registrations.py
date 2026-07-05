from app.database.orm import select, select_with_join
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
    RegistrationUpdate,
    StudentProof,
    AttendeeID
)
from app.core.settings import logger, settings
from fastapi import APIRouter, Depends, HTTPException, Request, status, BackgroundTasks


from app.database.connection import get_db_connection


api_router = APIRouter(tags=["registrations"])
base_url = settings.base_url.rstrip("/")
base_url = f"{base_url}/{settings.root_path.strip('/')}" if settings.root_path else base_url


@api_router.post("/register/{event_code}", status_code=status.HTTP_201_CREATED)
async def register_for_event(request: Request, registration: RegistrationCreate, event_code: str, background_tasks: BackgroundTasks, db=Depends(get_db_connection), is_student="No"):
    """
    Register a user for an event.
    """
    try:
        auth = request.headers.get("Authorization")
        event_existing = await select_with_join(db, table="events", join_table="tickets", join_condition="events.id = tickets.event_id", filter={"code": event_code.upper(), "tickets.id": registration.ticket_id}, columns=["tickets.event_id", "tickets.id", "tickets.name", "tickets.price", "tickets.quantity"])
        if not event_existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="event or ticket does not exist")
        if event_existing[0]["quantity"] < 1 or event_existing[0]["quantity"] < registration.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Not enough slots available for the selected ticket. Available quantity: {event_existing[0]['quantity']}")

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

        success_page_url = registration.success_page_url if registration.success_page_url and registration.success_page_url.startswith(
            "http") else f"{base_url}/checkout/payment-success"
        cancel_page_url = registration.cancel_page_url if registration.cancel_page_url and registration.cancel_page_url.startswith(
            "http") else f"{base_url}/checkout/payment-cancel"

        payment_data = {
            "amount": registration.ticket_price * registration.quantity,
            "callback_url": f"{base_url}/webhooks/paydunya/callback",
            "description": f"Registration for {event_code.upper()} - {registration.full_name}",
            "unit_price": registration.ticket_price,
            "quantity": registration.quantity,
            "name": registration.ticket_type,
            "success_page_url": success_page_url,
            "cancel_page_url": cancel_page_url
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{base_url}/checkout/payment", headers={"Authorization": auth}, json=payment_data)
            response.raise_for_status()
            result = response.json()
            payment_token = result.get("payment_url").split(
                "/")[-1]

            payment_link = result.get("payment_url")
            payment_reference = payment_token

            background_tasks.add_task(
                create_registration, request.app.state.db_pool, registration, payment_link, payment_reference, event_existing[0]["event_id"], is_student)

            return result
    except Exception as e:
        logger.error(f"Error creating registration: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.post("/registrations/student/approve")
async def _approve_student_registration(registration_id: AttendeeID, db=Depends(get_db_connection)):
    try:
        from app.utils.registrations import approve_student_registration
        result = await approve_student_registration(db, registration_id.attendee_id)
        return result
    except Exception as e:
        logger.error(f"Error approving student registration: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")
