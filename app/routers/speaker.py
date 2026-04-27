from app.utils.speaker import (add_speaker, get_all_speakers, get_speaker_by_id,
                               get_speakers_by_event, get_featured_speakers_by_event)
from app.schemas.models import (
    MessageResponse,
    SpeakerCreate,
    SpeakerSummary,
    SpeakerUpdate,
)
from app.core.settings import logger
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from app.database.connection import get_db_connection


api_router = APIRouter(prefix="/speakers", tags=["speakers"])


@api_router.get("/list/{event_code}", response_model=list[SpeakerSummary])
async def list_speakers(event_code: str, db=Depends(get_db_connection)):
    """
    List all speakers for a specific event.
    """
    try:
        speakers = await get_speakers_by_event(db, event_code)
        if not speakers:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No speakers yet please check back later")
        return speakers
    except Exception as e:
        logger.error(f"Error retrieving speakers: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.get("/featured/{event_code}", response_model=list[SpeakerSummary])
async def list_featured_speakers(event_code: str, db=Depends(get_db_connection)):
    """
    List all featured speakers for a specific event.
    """
    try:
        speakers = await get_featured_speakers_by_event(db, event_code)
        if not speakers:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No featured speakers yet please check back later")
        return speakers
    except Exception as e:
        logger.error(f"Error retrieving featured speakers: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.post("/add_new_speaker/{event_code}", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def add_new_speaker(speaker: SpeakerCreate, event_code: str, background_tasks: BackgroundTasks, db=Depends(get_db_connection)):
    """
    Add a new speaker to an event.
    """
    try:
        result = await add_speaker(db, speaker, event_code, background_tasks)
        return result
    except Exception as e:
        logger.error(f"Error adding speaker: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")
