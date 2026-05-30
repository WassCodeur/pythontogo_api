import httpx
from fastapi import APIRouter, Depends, HTTPException, Request

from app.schemas.models import TicketSubmissionPayload
from app.core.settings import settings, logger
from app.core.imagekit import upload_image_base64_url

app_router = APIRouter(prefix="/helper", tags=["submissions"])


base_url = settings.base_url.rstrip("/")
base_url = f"{base_url}/{settings.root_path.strip('/')}" if settings.root_path else base_url


@app_router.post("/ticket/submit/{event_code}")
async def submit_ticket(request: Request, payload: TicketSubmissionPayload, event_code: str):
    try:
        # TODO - Coupon code validation can be added here if needed
        # TODO: Add validation for the payload if needed

        auth = request.headers.get("Authorization")
        header = {
            "Authorization": auth
        }
        if not auth or not auth.startswith("Bearer "):
            raise HTTPException(
                status_code=401, detail="Unauthorized")
        # Here you can add additional validation for the payload if needed
        registration_data = {
            "full_name": payload.buyer.fullName,
            "email": payload.buyer.email,
            "whatsapp_number": payload.buyer.whatsapp,
            "ticket_type": payload.ticket.name,
            "ticket_id": payload.ticket.id,
            "ticket_price": payload.ticket.unitPrice,
            "quantity": payload.quantity,
            "attendance_status": "pending",
            "payment_status": "pending",
            "dietary_restrictions": payload.buyer.dietaryRestrictions,
            "payment_reference": "pending",
            "payment_link": "pending",
            "agreed_to_code_of_conduct": payload.consent.codeOfConduct,
            "agreed_to_privacy_policy": payload.consent.privacyPolicy,
            "shared_with_sponsors": payload.consent.partnerSharing,
            "success_page_url": None,
            "cancel_page_url": None
        }
        is_student = payload.ticket.isStudent or False
        if is_student:
            studentProof = payload.studentProof
            MIME_EXTENSION_MAP = {
                "image/jpeg": "jpg",
                "image/png": "png",
                "image/gif": "gif",
                "application/pdf": "pdf"
            }
            file_extension = MIME_EXTENSION_MAP.get(studentProof.mimeType)
            if not file_extension:
                raise HTTPException(
                    status_code=400, detail="Unsupported file type for student proof")
            image_name = f"{payload.buyer.fullName}_{payload.ticket.id}.{file_extension}"
            try:
                imagekitresponse = upload_image_base64_url(
                    image_name, studentProof.base64, folder="student_ids")
                registration_data["file_url"] = imagekitresponse.url
                registration_data["file_type"] = studentProof.mimeType
            except Exception as e:
                logger.error(f"Error uploading student proof: {str(e)}")
                raise HTTPException(
                    status_code=500, detail="Failed to upload student proof")

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{base_url}/register/{event_code}?is_student={is_student}", headers=header, json=registration_data)
            # Debugging line to check the response
            response_data = response.json()
            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code, detail="Failed to submit ticket")
        return response_data
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error processing ticket submission: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error processing ticket submission: {str(e)}")
