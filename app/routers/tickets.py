from app.utils.tickets import create_ticket, get_tickets_by_event, get_ticket_by_id, update_ticket
from app.schemas.models import (
    MessageResponse,
    TicketCreate,
    TicketSummary,
    TicketUpdate
)
from fastapi import APIRouter, BackgroundTasks, Depends, status, HTTPException

from app.database.connection import get_db_connection


api_router = APIRouter(prefix="/tickets", tags=["tickets"])


@api_router.post("/create/{event_code}", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket_endpoint(ticket: TicketCreate, event_code: str, background_tasks: BackgroundTasks, db=Depends(get_db_connection)):
    """
    Create a new ticket for an event.
    """
    try:
        ticket = ticket.model_dump(mode="json")
        result = await create_ticket(db, ticket, event_code)
        return result
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.get("/list/{event_code}", response_model=list[TicketSummary])
async def list_tickets(event_code: str, db=Depends(get_db_connection)):
    """
    List all tickets for a specific event.
    """
    try:
        tickets = await get_tickets_by_event(db, event_code)
        if not tickets:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No slot available for this event yet please check back later")
        return tickets
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")
