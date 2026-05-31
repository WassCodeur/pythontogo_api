from urllib.parse import parse_qs
from fastapi import FastAPI, Request
import hashlib
from fastapi import APIRouter, Request, HTTPException, status, Depends, BackgroundTasks
from app.core.settings import settings
from app.database.connection import get_db_connection
from app.schemas.models import RegistrationUpdate
from app.webhooks.helper import phpformat_to_json
from app.utils.registrations import update_registration


api_router = APIRouter(prefix="/webhooks", tags=["webhooks"])


def verify_paydunya_hash(hash):
    # Implement your signature verification logic here
    # For example, you might compare the hash with a computed hash of the payload
    expected_hash = hashlib.sha512(
        settings.paydunya_master_key.encode()).hexdigest()
    return hash == expected_hash


@api_router.post("/paydunya/callback")
async def payments_callback(request: Request, background_tasks: BackgroundTasks, db=Depends(get_db_connection)):
    try:
        body = await request.body()
        text = body.decode()

        parsed = parse_qs(text)
        payload = {}

        phpformat_to_json(parsed, payload)

        hash = payload.get("data", {}).get("hash")
        payment_status = payload.get("data", {}).get("status", "")
        token = payload.get("data", {}).get("invoice", {}).get("token")

        if not hash or not verify_paydunya_hash(hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Unauthorized source")

        if payment_status == "completed":
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payment")

            updated_data = {
                "payment_status": "completed",
                "payment_reference": token,
                "payment_link": payload.get("data", {}).get("receipt_url", "")
            }

            background_tasks.add_task(
                update_registration, db, updated_data, request)

            return {"message": "callback received successfully"}

            # Here you would typically verify the payload, check the payment status,
            # and update your database accordingly.

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Payment not completed")

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error processing callback")


if __name__ == "__main__":
    hs = hashlib.sha512(
        settings.paydunya_master_key.encode()).hexdigest()
    print("Expected Hash:", hs)
