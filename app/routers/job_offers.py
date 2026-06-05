from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from app.database.connection import get_db_connection
from app.schemas.models import JobOfferCreate, JobOfferSummary, JobOfferUpdate, MessageResponse
from app.utils.job_offers import (
    add_job_offer,
    delete_job_offer,
    get_active_job_offers,
    get_all_job_offers,
    get_job_offer_by_id,
    update_job_offer,
)
from app.core.settings import logger


api_router = APIRouter(prefix="/job-offers", tags=["job-offers"])


@api_router.post("/create", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_job_offer(
    job_offer: JobOfferCreate,
    background_tasks: BackgroundTasks,
    db=Depends(get_db_connection),
):
    """Create a new job offer."""
    try:
        return await add_job_offer(db, job_offer, background_tasks)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.get("/list/active", response_model=list[JobOfferSummary])
async def list_active_job_offers(db=Depends(get_db_connection)):
    """List all active job offers."""
    try:
        job_offers = await get_active_job_offers(db)
        if not job_offers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active job offers found",
            )
        return job_offers
    except Exception as e:
        logger.error(f"Error listing active job offers: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.get("/list", response_model=list[JobOfferSummary])
async def list_all_job_offers(db=Depends(get_db_connection)):
    """List all job offers (admin)."""
    try:
        return await get_all_job_offers(db)
    except Exception as e:
        logger.error(f"Error listing all job offers: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.get("/{job_offer_id}", response_model=JobOfferSummary)
async def get_job_offer(job_offer_id: str, db=Depends(get_db_connection)):
    """Retrieve a job offer by its ID."""
    try:
        return await get_job_offer_by_id(db, job_offer_id)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.put("/update/{job_offer_id}", response_model=MessageResponse)
async def update_job_offer_details(
    job_offer_id: str,
    job_offer_update: JobOfferUpdate,
    background_tasks: BackgroundTasks,
    db=Depends(get_db_connection),
):
    """Update an existing job offer."""
    try:
        return await update_job_offer(db, job_offer_id, job_offer_update, background_tasks)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.delete("/delete/{job_offer_id}", response_model=MessageResponse)
async def delete_job_offer_by_id(
    job_offer_id: str,
    background_tasks: BackgroundTasks,
    db=Depends(get_db_connection),
):
    """Delete a job offer by its ID."""
    try:
        return await delete_job_offer(db, job_offer_id, background_tasks)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")
