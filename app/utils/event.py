from app.database.orm import select, insert, update, select_with_join, delete
from fastapi import HTTPException, status


async def add_event(db, payload: dict):
    try:
        await insert(db, "events", payload)
    except Exception as e:
        # TODO logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error adding event")


async def delete_event(db, event_id: str):
    try:
        await delete(db, "events", filter={"id": event_id})
    except Exception as e:
        # TODO logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error deleting event")


async def get_event_by_code(db, event_code: str):
    try:
        event_code = event_code.upper()
        event = await select(db, "events", filter={"code": event_code})
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Event with code {event_code} not found")
        return event[0]
    except Exception as e:
        # TODO logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error retrieving event")


async def get_events(db):
    try:
        events = await select(db, "events")
        return events
    except Exception as e:
        # TODO logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error retrieving events")


async def update_event(db, event_code: str, payload: dict):
    try:
        event_code = event_code.upper()
        existing = await select(db, "events", filter={"code": event_code})
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Event with code {event_code} not found")
        await update(db, "events", payload, filter={"code": event_code})
    except Exception as e:
        # TODO logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error updating event")
