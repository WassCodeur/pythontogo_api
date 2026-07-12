from app.database.orm import select, insert, update, delete, select_with_join
from app.schemas.models import TrackCreate, TrackUpdate
from fastapi import BackgroundTasks, HTTPException
from uuid import uuid4
from app.utils.helpers import remove_null_values
from app.core.settings import logger


async def generate_voucher_code(db, voucher_data):
    """
    Generate a unique voucher code.
    """
    id = uuid4().hex[:4].upper()

    prefix = voucher_data.get("prefix", "PYCONTG")

    cleaned_prefix = prefix.replace(
        " ", "-").rstrip("-").upper() if prefix else "PYCONTG"
    voucher_code = f"{cleaned_prefix}-{id}" if cleaned_prefix else id

    existing_voucher = await select(db, "vouchers", filter={"code": voucher_code, "is_active": True})
    if existing_voucher:
        logger.info(
            f"Voucher code {voucher_code} already exists. Generating a new one.")
        return await generate_voucher_code(db, voucher_data)

    voucher_data["code"] = voucher_code
    # Remove prefix from the data to be inserted
    voucher_data.pop("prefix", None)
    await insert(db, "vouchers", voucher_data)
    return voucher_code


async def update_voucher(db, voucher_id, voucher_data):
    """
    Update an existing voucher.
    """
    try:
        existing_voucher = await select(db, "vouchers", filter={"id": voucher_id})
        if not existing_voucher:
            raise HTTPException(status_code=404, detail="Voucher not found")

        cleaned_data = remove_null_values(voucher_data)
        await update(db, "vouchers", cleaned_data, filter={"id": voucher_id})
        return {"message": "Voucher updated successfully"}
    except Exception as e:
        logger.error(f"Error updating voucher: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def delete_voucher(db, voucher_id):
    """
    Delete an existing voucher.
    """
    try:
        existing_voucher = await select(db, "vouchers", filter={"id": voucher_id})
        if not existing_voucher:
            raise HTTPException(status_code=404, detail="Voucher not found")

        await delete(db, "vouchers", filter={"id": voucher_id})
        return {"message": "Voucher deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting voucher: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_voucher_by_code(db, voucher_code):
    """
    Retrieve a voucher by its code.
    """
    try:
        existing_voucher = await select(db, "vouchers", filter={"code": voucher_code, "is_active": True})
        if not existing_voucher:
            raise HTTPException(status_code=404, detail="Voucher not found")

        return existing_voucher[0]
    except Exception as e:
        logger.error(f"Error retrieving voucher")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def apply_voucher_to_registration(db, registration_id, voucher_code):
    """
    Apply a voucher to a registration.
    """
    try:
        existing_voucher = await select(db, "vouchers", filter={"code": voucher_code, "is_active": True})
        if not existing_voucher:
            raise HTTPException(status_code=404, detail="Invalid voucher code")

        existing_registration = await select(db, "registrations", filter={"id": registration_id})
        if not existing_registration:
            raise HTTPException(
                status_code=404, detail="Registration not found")

        await update(db, "registrations", {"voucher_id": existing_voucher[0]["id"]}, filter={"id": registration_id})
        return {"message": "Voucher applied to registration successfully"}
    except Exception as e:
        logger.error(f"Error applying voucher to registration: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def validate_voucher(request, voucher_code, ticket_id: str, event_id, user_email):
    """
    Validate a voucher for a specific ticket, event, and user.
    """
    try:

        async with request.app.state.db_pool.connection() as db:
            existing_voucher = await select(db, "vouchers", filter={"code": voucher_code, "is_active": True})
            if not existing_voucher:
                return None

            voucher = existing_voucher[0]
            ticket_id = str(ticket_id)
            event_id = str(event_id)
            current_time = request.app.state.current_time

            # TODO: Implement additional validation logic based on your business rules

            if voucher.get("valid_from") and voucher.get("valid_until"):
                if not (voucher["valid_from"] <= current_time <= voucher["valid_until"]):
                    logger.info(
                        f"Voucher {voucher_code} is not valid at the current time.")
                    logger.info(
                        f"Current time: {current_time}, Valid from: {voucher['valid_from']}, Valid until: {voucher['valid_until']}")
                    return None
            if not voucher.get("is_active", False):
                return None
            if voucher.get("applicable_ticket_ids") and ticket_id not in voucher["applicable_ticket_ids"]:

                return None

            # Check if the voucher is applicable to the event
            if voucher.get("applicable_event_ids") and event_id not in voucher["applicable_event_ids"]:
                logger.info(
                    f"Voucher {voucher_code} is not applicable to event {event_id}")
                return None

            # Check if the voucher is applicable to the user email
            if voucher.get("applicable_user_emails") and user_email not in voucher["applicable_user_emails"]:
                logger.info(
                    f"Voucher {voucher_code} is not applicable to user email {user_email}")
                return None
            if voucher.get("already_used_by_user_emails") and user_email in voucher["already_used_by_user_emails"]:
                logger.info(
                    f"Voucher {voucher_code} has already been used by user email {user_email}")
                return None
            # Check if the voucher has remaining uses
            if voucher.get("number_of_uses_left", 0) <= 0:
                logger.info(f"Voucher {voucher_code} has no remaining uses.")
                return None

            return voucher
    except Exception as e:
        logger.error(f"Error validating voucher: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def calculate_discounted_price(original_price, discount_percentage, discount_amount=None, discount_type="percentage"):
    """
    Calculate the discounted price based on the original price and discount details.
    """
    from decimal import Decimal, ROUND_HALF_UP

    original_price = Decimal(str(original_price))
    discount_percentage = Decimal(str(discount_percentage))

    if discount_percentage < 0 or discount_percentage > 100:
        raise ValueError("Discount percentage must be between 0 and 100")

    amount = (
        original_price
        * (Decimal("1") - discount_percentage / Decimal("100"))
    ).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    return int(amount)
