from app.database.orm import insert, select, update, select_with_join
from app.schemas.models import MessageResponse, RegistrationCreate, RegistrationUpdate, RegistrationSummary
from uuid import uuid4
from app.utils.tickets import update_ticket, get_ticket_by_id


async def create_registration(db, registration):
    """
    Create a new registration for an event.
    """

    await insert(db, "registrations", registration)
    return MessageResponse(message="Registration successful")


async def update_registration(db, registration_update: RegistrationUpdate):
    """
    Update an existing registration.
    """
    payment_reference = registration_update.get("payment_reference", "")
    existing_registration = await select(db, "registrations", filter={"payment_reference": payment_reference})
    existing_registration = await select_with_join(db, table="registrations", join_table="tickets", join_condition="registrations.ticket_id = tickets.id", filter={"registrations.payment_reference": payment_reference}, columns=["registrations.full_name", "registrations.email", "registrations.whatsapp_number", "registrations.ticket_quantity", "registrations.ticket_id", "tickets.quantity", "tickets.name"])
    if not existing_registration:
        return MessageResponse(message="Registration not found")

    ticket_available = existing_registration[0]['quantity'] - \
        existing_registration[0]['ticket_quantity']
    update_data = registration_update
    update_data['ticket_type'] = existing_registration[0]['name']
    await update(db, "registrations", filter={"payment_reference": payment_reference}, data=update_data)
    await update_ticket(db, existing_registration[0]['ticket_id'], {"quantity": ticket_available})
    # TODO: implement logic to handle ticket quantity updates and ensure that the ticket availability is updated accordingly when a registration is updated (e.g., if the ticket quantity is increased, check if there are enough tickets available and update the ticket quantity in the database; if the ticket quantity is decreased, update the ticket quantity in the database accordingly)
    # send email notification to user about registration update (e.g., payment confirmation)
    return MessageResponse(message="Registration updated successfully")
