from app.database.orm import select, insert, update, delete, select_with_join
from app.schemas.models import SpeakerCreate, SpeakerUpdate
from fastapi import BackgroundTasks, HTTPException
from uuid import uuid4
from app.utils.helpers import remove_null_values
from app.core.settings import logger


async def get_all_speakers(db):
    """
    Retrieve all speakers from the database.
    """
    try:
        speakers = await select(db, "speakers")
        if not speakers:
            raise HTTPException(status_code=404, detail="No speakers found")
        return speakers
    except Exception as e:
        logger.error(f"Error retrieving speakers: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error: ")


async def get_speaker_by_id(db, speaker_id):
    """
    Retrieve a speaker by its ID.
    """
    try:
        speaker = await select(db, "speakers", filter={"id": speaker_id})
        if not speaker:
            return {}
        return speaker[0]
    except Exception as e:
        logger.error(f"Error retrieving speaker: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_speakers_by_event(db, event_code):
    try:
        event_code = event_code.strip().upper()

        speakers = await select_with_join(db, table="speakers", join_table="events",
                                          join_condition="speakers.event_id = events.id",
                                          columns=["speakers.full_name", "speakers.headline", "speakers.organization", "speakers.company_logo_url", "speakers.country", "speakers.bio", "speakers.photo_url", "speakers.social_links", "speakers.sessions",
                                                    "speakers.event_id", "speakers.created_at", "speakers.updated_at"],
                                          filter={"events.code": event_code})

        if not speakers:
            return []
        return speakers
    except Exception as e:
        logger.error(f"Error retrieving speakers: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error: ")


async def get_featured_speakers_by_event(db, event_code):
    """Retrieve all featured speakers for a specific event.
    """
    try:
        event_code = event_code.strip().upper()

        speakers = await select_with_join(db, table="speakers", join_table="events",
                                          join_condition="speakers.event_id = events.id",
                                          columns=["speakers.full_name", "speakers.headline", "speakers.organization", "speakers.company_logo_url", "speakers.country", "speakers.bio", "speakers.photo_url", "speakers.social_links", "speakers.sessions",
                                                    "speakers.event_id", "speakers.created_at", "speakers.updated_at"],
                                          filter={"events.code": event_code, "speakers.is_featured": True})

        if not speakers:
            return []
        return speakers
    except Exception as e:
        logger.error(f"Error retrieving featured speakers: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error: ")


async def add_speaker(db, speaker: SpeakerCreate, event_code: str, background_tasks: BackgroundTasks):
    """
    Add a new speaker to the database.
    """
    try:
        event_code = event_code.strip().upper()
        speaker_id = str(uuid4())
        speaker_data = speaker.model_dump()
        speaker_data["id"] = speaker_id
        event_id = (await select(db, "events", filter={"code": event_code}, columns=["id"]))[0]["id"]
        if not event_id:
            raise HTTPException(status_code=404, detail="Event not found")
        speaker_data["event_id"] = event_id
        background_tasks.add_task(insert, db, "speakers", speaker_data)

        return {"message": "Speaker created successfully"}
    except Exception as e:
        logger.error(f"Error creating speaker: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error: ")
