from fastapi import APIRouter, BackgroundTasks, Depends, status, HTTPException
from app.utils.sponsor_partner import (add_sponsor_partner, get_sponsors_partners_by_event,
                                       get_sponsors_partners, _update_partner_sponsor, delete_sponsor_partner)


from app.schemas.models import (
    HealthResponse,
    MessageResponse,
    PartnerSponsorUpdate,

    PartnershipSponsorshipInquiry,
    SponsorsPartnersList,


)
from app.database.connection import get_db_connection


api_router = APIRouter(prefix="/partners-sponsors",
                       tags=["Partners & Sponsors"])


@api_router.post("/inquiry/{event_code}", response_model=MessageResponse, status_code=status.HTTP_202_ACCEPTED)
async def partnership_sponsorship_inquiry(event_code: str, payload: PartnershipSponsorshipInquiry, background_tasks: BackgroundTasks, db=Depends(get_db_connection)):
    try:
        event_code = event_code.upper()
        background_tasks.add_task(
            add_sponsor_partner, db, payload.model_dump(), event_code)
        return {
            "message": f"Company {payload.name} partnership/sponsorship request received successfully and is being processed"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing partnership/sponsorship request: {str(e)}")


@api_router.get("/", response_model=SponsorsPartnersList)
async def get_all_partners_sponsors(db=Depends(get_db_connection)):
    try:
        partners_sponsors = await get_sponsors_partners(db)
        return partners_sponsors
    except Exception as e:
        # TODO - logging the error can be done here
        raise HTTPException(
            status_code=500, detail="Error retrieving partners/sponsors")


@api_router.get("/{event_code}", response_model=SponsorsPartnersList)
async def get_partners_sponsors(event_code: str, db=Depends(get_db_connection)):
    try:
        event_code = event_code.upper()
        partners_sponsors = await get_sponsors_partners_by_event(db, event_code=event_code)

        return partners_sponsors
    except Exception as e:
        # TODO - logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail="Error retrieving partners/sponsors")


@api_router.put("/{partner_id}", response_model=MessageResponse)
async def update_partner_sponsor(partner_id: str, payload: PartnerSponsorUpdate, background_tasks: BackgroundTasks, db=Depends(get_db_connection)):
    try:
        data_to_update = {k: v for k,
                          v in payload.model_dump().items() if v is not None}
        background_tasks.add_task(
            _update_partner_sponsor, db, partner_id, data_to_update)
        return {"message": "Partner/Sponsor updated successfully"}
    except Exception as e:
        # TODO - logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail="Error updating partner/sponsor")


@api_router.delete("/{partner_id}", response_model=MessageResponse)
async def delete_partner_sponsor(partner_id: str, db=Depends(get_db_connection)):
    try:
        await delete_sponsor_partner(db, partner_id=partner_id)
        return {"message": "Partner/Sponsor deleted successfully"}
    except Exception as e:
        # TODO - logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail="Error deleting partner/sponsor")


@api_router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="healthy")
