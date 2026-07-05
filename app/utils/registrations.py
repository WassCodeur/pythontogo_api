from app.database.orm import insert, select, update, select_with_join
from app.schemas.models import MessageResponse, RegistrationCreate, RegistrationUpdate, RegistrationSummary
from uuid import uuid4, UUID
from app.utils.date_format import format_date
from app.utils.tickets import update_ticket, get_ticket_by_id
from app.utils.send_email import send_email_for_confirme_your_ticket_purchase, send_email_for_pass, send_email_for_student_proof_of_enrollment
from json import dumps
from fastapi import HTTPException
from app.core.settings import logger


async def create_registration(db_pool, registration: RegistrationCreate, payment_link, payment_reference, event_id: UUID, is_student=False):
    """
    Create a new registration for an event.
    """
    _to = registration.email
    _action_url = payment_link
    _action_text = "Confirm Your Ticket Purchase"
    _first_name = registration.full_name.split()[0]
    last_name = registration.full_name.split()[-1]
    registration_id = uuid4()

    registration_data = {
        "id": str(registration_id),
        "event_id": event_id,
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
        "payment_reference": payment_reference,
        "payment_link": payment_link,
        "agreed_to_code_of_conduct": registration.agreed_to_code_of_conduct,
        "agreed_to_privacy_policy": registration.agreed_to_privacy_policy,
        "shared_with_sponsors": registration.shared_with_sponsors
    }

    if is_student in ["yes", "Yes", "YES", True, "true", "True", "TRUE"]:
        student_proof = {
            "id": str(uuid4()),
            "full_name": registration.full_name,
            "email": registration.email,
            "registration_id": str(registration_id),
            "file_url": registration.file_url,
            "file_type": registration.file_type,
            "is_reviewed": False,
            "is_approved": False
        }

    async with db_pool.connection() as connection:
        await insert(connection, "registrations", registration_data)

        if is_student in ["yes", "Yes", "YES", True, "true", "True", "TRUE"]:
            student_proof = {
                "id": str(uuid4()),
                "full_name": registration.full_name,
                "email": registration.email,
                "registration_id": str(registration_id),
                "file_url": registration.file_url,
                "file_type": registration.file_type,
                "is_reviewed": False,
                "is_approved": False
            }
            await insert(connection, "student_proofs", student_proof)
    await send_email_for_confirme_your_ticket_purchase(to=_to, action_url=_action_url, action_text=_action_text, first_name=_first_name, last_name=last_name)
    return MessageResponse(message="Registration successful")


async def update_registration(db_pool, redis_client, registration_update: RegistrationUpdate):
    """
    Update an existing registration.
    """
    payment_reference = registration_update.get("payment_reference", "")
    payment_id = payment_reference.replace("_", "")

    async with db_pool.connection() as db:

        existing_registration = await select_with_join(db, table="registrations", join_table="tickets", join_condition="registrations.ticket_id = tickets.id", filter={"registrations.payment_reference": payment_reference}, columns=["registrations.full_name", "registrations.id", "registrations.email", "registrations.whatsapp_number", "registrations.ticket_quantity", "registrations.payment_link", "registrations.ticket_id", "tickets.quantity", "tickets.name"])

        if not existing_registration:
            return MessageResponse(message="Registration not found")

        student_proof = await select(db, "student_proofs", filter={"registration_id": existing_registration[0]['id'], "full_name": existing_registration[0]['full_name'], "email": existing_registration[0]['email']}) if existing_registration else None

        ticket_available = existing_registration[0]['quantity'] - \
            existing_registration[0]['ticket_quantity']

        update_data = registration_update
        update_data['ticket_type'] = existing_registration[0]['name']

        await redis_client.set(f"ticket_registration_token:{payment_reference}", payment_reference, ex=3600)
        await update(db, "registrations", filter={"payment_reference": payment_reference}, data=update_data)
        await update_ticket(db, existing_registration[0]['ticket_id'], {"quantity": ticket_available})

        if student_proof:
            submission_date = format_date(student_proof[0]['created_at'])
            document_name = student_proof[0]['file_url'].split("/")[-1]
            document_url = student_proof[0]['file_url']
            send_email_for_student_proof_of_enrollment(to=existing_registration[0]['email'], first_name=existing_registration[0]['full_name'].split(
            )[0], full_name=existing_registration[0]['full_name'], proof_id=payment_id, submission_date=submission_date, document_name=document_name, document_url=document_url)
            return MessageResponse(message="Registration updated successfully")

        send_email_for_pass(to=existing_registration[0]['email'], first_name=existing_registration[0]['full_name'].split()[0], full_name=existing_registration[0]['full_name'],
                            ticket_id=payment_id, pass_type=existing_registration[0]['name'], number_of_slots=existing_registration[0]['ticket_quantity'])
    return MessageResponse(message="Registration updated successfully")


async def approve_student_registration(db, registration_id: str):
    """
    Approve a student registration.
    """
    try:
        registration = await select(db, "registrations", filter={"id": registration_id})
        print(f"Registration data: {registration}")
        student_reg = await select_with_join(db, table="registrations", join_table="student_proofs", join_condition="registrations.id = student_proofs.registration_id", filter={"registrations.id": registration_id}, columns=[
            "registrations.full_name", "registrations.email", "registrations.payment_reference", "registrations.ticket_type", "registrations.ticket_quantity", "student_proofs.file_url", "student_proofs.file_type", "student_proofs.is_reviewed", "student_proofs.is_approved"])
        if not student_reg:
            return MessageResponse(message="Registration not found")

        send_email_for_pass(to=student_reg[0]['email'], first_name=student_reg[0]['full_name'].split()[0], full_name=student_reg[0]['full_name'],
                            ticket_id=student_reg[0]['payment_reference'], pass_type=student_reg[0]['ticket_type'], number_of_slots=student_reg[0]['ticket_quantity'])

        await update(db, "student_proofs", filter={"registration_id": registration_id}, data={
            "is_reviewed": True, "is_approved": True})
        return MessageResponse(message="Student registration approved successfully")
    except Exception as e:
        logger.error(f"Error approving student registration: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import asyncio
    asyncio.run(
        approve_student_registration(db=None, registration_id="ccffa861-2993-4de8-8e0c-b6fdc660a989"))
