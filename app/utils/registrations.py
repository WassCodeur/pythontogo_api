from app.database.orm import insert, select, update, select_with_join
from app.schemas.models import MessageResponse, RegistrationCreate, RegistrationUpdate, RegistrationSummary
from uuid import uuid4
from app.utils.tickets import update_ticket, get_ticket_by_id
from app.utils.send_email import send_email_for_ticket_puchase_confirmation, send_email_for_confirme_your_ticket_purchase, send_email_for_pass


async def create_registration(db, registration, student_proof, is_student=False):
    """
    Create a new registration for an event.
    """
    _to = registration.get("email", "")
    _action_url = registration.get("payment_link", "")
    _action_text = "Confirm Your Ticket Purchase"
    _first_name = registration.get("full_name", "Pythonista").split()[0]
    last_name = registration.get("full_name", "Participant").split()[-1]

    await insert(db, "registrations", registration)
    if is_student:
        await insert(db, "student_proofs", student_proof)
    await send_email_for_confirme_your_ticket_purchase(to=_to, action_url=_action_url, action_text=_action_text, first_name=_first_name, last_name=last_name)
    return MessageResponse(message="Registration successful")


async def update_registration(db, registration_update: RegistrationUpdate):
    """
    Update an existing registration.
    """
    payment_reference = registration_update.get("payment_reference", "")
    payment_link = registration_update.get("payment_link", "")

    existing_registration = await select_with_join(db, table="registrations", join_table="tickets", join_condition="registrations.ticket_id = tickets.id", filter={"registrations.payment_reference": payment_reference}, columns=["registrations.full_name", "registrations.id", "registrations.email", "registrations.whatsapp_number", "registrations.ticket_quantity", "registrations.payment_link", "registrations.ticket_id", "tickets.quantity", "tickets.name"])

    if not existing_registration:
        return MessageResponse(message="Registration not found")

    student_proof = await select(db, "student_proofs", filter={"registration_id": existing_registration[0]['id'], "full_name": existing_registration[0]['full_name'], "email": existing_registration[0]['email']}) if existing_registration else None

    ticket_available = existing_registration[0]['quantity'] - \
        existing_registration[0]['ticket_quantity']

    update_data = registration_update
    update_data['ticket_type'] = existing_registration[0]['name']
    await update(db, "registrations", filter={"payment_reference": payment_reference}, data=update_data)
    await update_ticket(db, existing_registration[0]['ticket_id'], {"quantity": ticket_available})
    # send email notification to user about registration update (e.g., payment confirmation)
    action_url = payment_link
    action_text = "Download Your Ticket"
    if student_proof:
        # TODO: Send email to user about student proof review status if needed
        return MessageResponse(message="Registration updated successfully")
    send_email_for_pass(to=existing_registration[0]['email'], first_name=existing_registration[0]['full_name'].split()[0], full_name=existing_registration[0]['full_name'],
                        ticket_id=payment_reference.replace("_", ""), pass_type=existing_registration[0]['name'], number_of_slots=existing_registration[0]['ticket_quantity'])
    return MessageResponse(message="Registration updated successfully")
