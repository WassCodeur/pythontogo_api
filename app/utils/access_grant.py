from app.database.orm import insert, select, select_with_join
from app.core.settings import logger
from app.core.imagekit import upload_image_base64_url


async def create_access_grant(db_pool, access_grant_data, event_code: str):
    async with db_pool.connection() as conn:
        event_exist = await select(conn, "events", ["id"], {"code": event_code})
        if not event_exist:
            logger.error("event doesn't exist")
            return {"error": "Event doesn't exist."}

        grant_applcation_exist = await select_with_join(conn, "access_grants", "events", "access_grants.event_id = events.id", ["access_grants.id"],  {"email": access_grant_data["email"]})
        if grant_applcation_exist:
            logger.warning("grant application already exists")
            return {"Warning": "Grant application already exists for this email and event."}

        access_grant = {
            "first_name": access_grant_data["first_name"],
            "last_name": access_grant_data["last_name"],
            "email": access_grant_data["email"],
            "gender": access_grant_data.get("gender", "Not specified"),
            "phone_number": access_grant_data.get("whatsapp"),
            "location": access_grant_data.get("location"),
            "country": access_grant_data.get("country"),
            "python_journey": access_grant_data.get("python_journey"),
            "need_ticket": access_grant_data.get("need_ticket", False),
            "need_transport": access_grant_data.get("need_transport", False),
            "need_accommodation": access_grant_data.get("need_accommodation", False),
            "support_details": access_grant_data.get("support_details"),
            "grant_consent": access_grant_data.get("grant_consent"),
            "event_id": event_exist[0]["id"],
            "is_student": access_grant_data.get("is_student", False),
            "student_proof_url": None,
            "is_approved": False,
            "is_reviewed": False,
            "comment": "",
        }

        if access_grant_data.get("is_student") and access_grant_data.get("student_proof"):
            student_proof = access_grant_data["student_proof"]
            MIME_EXTENSION_MAP = {
                "image/jpeg": "jpg",
                "image/png": "png",
                "image/gif": "gif",
                "application/pdf": "pdf"
            }
            file_extension = MIME_EXTENSION_MAP.get(
                student_proof.get("mimeType"))
            if not file_extension:
                logger.error("Unsupported file type for student proof")
                return {"error": "Unsupported file type for student proof. Allowed types: jpg, jpeg, png, pdf."}

            image_name = f"{access_grant_data['first_name']}_{access_grant_data['last_name']}_student_proof.{file_extension}"
            upload_response = upload_image_base64_url(
                image_name, student_proof["base64"], folder="access_grants/student_proofs")
            if upload_response and upload_response.url:
                access_grant["student_proof_url"] = upload_response.url
            else:
                logger.error("Failed to upload student proof")
                return {"error": "Failed to upload student proof."}

        await insert(conn, "access_grants", access_grant)

        return {"message": "Access grant request submitted successfully."}
