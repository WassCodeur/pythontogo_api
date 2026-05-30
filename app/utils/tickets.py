from fastapi import HTTPException, logger

from app.database.orm import insert, select, update, select_with_join
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


async def get_tickets_by_event(db, event_code):
    """
    Retrieve all tickets for a specific event using the event code.
    """
    try:
        tickets = await select_with_join(
            db,
            "tickets",
            "events",
            "tickets.event_id = events.id",
            columns=["tickets.id", "tickets.quantity",
                     "tickets.price", "tickets.name", "tickets.description", "tickets.early_bird_price"],
            filter={"events.code": event_code.strip().upper()}
        )
        return tickets
    except Exception as e:
        # TODO sending email to admin about error during processing the request can be done here
        logger.error(f"Error retrieving tickets by event code: {str(e)}")
        raise HTTPException(
            status_code=500, detail="oups! something went wrong while retrieving tickets for the event")


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
