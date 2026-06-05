from uuid import uuid4

from fastapi import BackgroundTasks, HTTPException

from app.database.orm import delete, insert, select, update
from app.schemas.models import JobOfferCreate, JobOfferUpdate
from app.core.settings import logger
from app.utils.helpers import remove_null_values


async def get_all_job_offers(db):
    try:
        job_offers = await select(db, "job_offers")
        if not job_offers:
            raise HTTPException(status_code=404, detail="No job offers found")
        return job_offers
    except Exception as e:
        logger.error(f"Error retrieving job offers: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_active_job_offers(db):
    try:
        job_offers = await select(db, "job_offers", filter={"is_active": True})
        return job_offers or []
    except Exception as e:
        logger.error(f"Error retrieving active job offers: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_job_offer_by_id(db, job_offer_id: str):
    try:
        job_offer = await select(db, "job_offers", filter={"id": job_offer_id})
        if not job_offer:
            raise HTTPException(status_code=404, detail="Job offer not found")
        return job_offer[0]
    except Exception as e:
        logger.error(f"Error retrieving job offer {job_offer_id}: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def add_job_offer(db, job_offer: JobOfferCreate, background_tasks: BackgroundTasks):
    try:
        job_offer_data = job_offer.model_dump(mode="json")

        existing = await select(db, "job_offers", filter={
            "title": job_offer_data["title"],
            "company": job_offer_data["company"],
        })
        if existing:
            raise HTTPException(
                status_code=400,
                detail="A job offer with the same title and company already exists",
            )

        job_offer_data["id"] = str(uuid4())
        background_tasks.add_task(insert, db, "job_offers", job_offer_data)
        return {"message": "Job offer created successfully"}
    except Exception as e:
        logger.error(f"Error adding job offer: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def update_job_offer(db, job_offer_id: str, job_offer_update: JobOfferUpdate, background_tasks: BackgroundTasks):
    try:
        update_data = remove_null_values(job_offer_update.model_dump(mode="json"))
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields provided for update")

        existing = await select(db, "job_offers", filter={"id": job_offer_id})
        if not existing:
            raise HTTPException(status_code=404, detail="Job offer not found")

        background_tasks.add_task(update, db, "job_offers", update_data, filter={"id": job_offer_id})
        return {"message": "Job offer updated successfully"}
    except Exception as e:
        logger.error(f"Error updating job offer {job_offer_id}: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def delete_job_offer(db, job_offer_id: str, background_tasks: BackgroundTasks):
    try:
        existing = await select(db, "job_offers", filter={"id": job_offer_id})
        if not existing:
            raise HTTPException(status_code=404, detail="Job offer not found")

        background_tasks.add_task(delete, db, "job_offers", filter={"id": job_offer_id})
        return {"message": "Job offer deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting job offer {job_offer_id}: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")
