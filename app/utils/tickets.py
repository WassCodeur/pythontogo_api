from fastapi import HTTPException

from app.database.orm import insert, select, update
from app.utils.event import get_event_by_code


async def create_ticket(db, ticket, event_code):
    """
    Create a new ticket for an event.
    """
    event = await get_event_by_code(db, event_code)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    ticket["event_id"] = event["id"]
    await insert(db, "tickets", ticket)
    return {"message": "Ticket created successfully"}


async def get_tickets_by_event(db, event_id):
    """
    Retrieve all tickets for a specific event.
    """
    tickets = await select(db, "tickets", filter={"event_id": event_id})
    return tickets


async def get_ticket_by_id(db, ticket_id):
    """
    Retrieve a ticket by its ID.
    """
    ticket = await select(db, "tickets", filter={"id": ticket_id})
    if not ticket:
        return {}
    return ticket[0]


async def update_ticket(db, ticket_id, update_data):
    """
    Update an existing ticket.
    """
    await update(db, "tickets", filter={"id": ticket_id}, data=update_data)
    return {"message": "Ticket updated successfully"}
