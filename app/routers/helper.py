import httpx
from fastapi import APIRouter, Depends, HTTPException, Request

from app.schemas.models import TicketSubmissionPayload, RegistrationCreate
from app.core.settings import settings, logger
from app.core.imagekit import upload_image_base64_url


def submit_ticket(payload: TicketSubmissionPayload) -> tuple[RegistrationCreate, bool]:
    try:
        # TODO - Coupon code validation can be added here if needed
        # TODO: Add validation for the payload if needed

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
            "success_page_url": payload.success_page_url,
            "cancel_page_url": payload.cancel_page_url
        }
        is_student = payload.ticket.isStudent or False
        if is_student in ["yes", "Yes", "YES", True, "true", "True", "TRUE"]:
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
            document_name = f"{payload.buyer.fullName}_{payload.ticket.id[:8]}_proof.{file_extension}"
            try:
                imagekitresponse = upload_image_base64_url(
                    document_name, studentProof.base64, folder="student_ids")
                registration_data["file_url"] = imagekitresponse.url
                registration_data["file_type"] = studentProof.mimeType
            except Exception as e:
                logger.error(f"Error uploading student proof: {str(e)}")
                raise HTTPException(
                    status_code=500, detail="Failed to upload student proof")

        return registration_data, is_student
    except Exception as e:
        # Log the error for debugging
        import traceback
        traceback.print_exc()
        logger.error(f"Error processing ticket submission")
        raise HTTPException(
            status_code=500, detail=f"Error processing ticket submission")
