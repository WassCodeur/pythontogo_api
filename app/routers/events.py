from fastapi import APIRouter, BackgroundTasks, Depends, status, HTTPException
from app.utils.event import (
    add_event, get_events, get_event_by_code, update_event, delete_event)
from app.schemas.models import (
    EventBase, EventSummary, MessageResponse)


from app.database.connection import get_db_connection

api_router = APIRouter(prefix="/events", tags=["events"])


@api_router.post("/create", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: EventBase, db=Depends(get_db_connection)):
    try:
        event_code = event.code.upper()
        existing_event = get_event_by_code(db, event_code)
        if existing_event:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Event with code {event_code} already exists")
        new_event = add_event(db, event.model_dump())
        return MessageResponse(message="Event created successfully")
    except Exception as e:
        # TODO - logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error creating event")


@api_router.get("/list", response_model=list[EventSummary])
def list_events(db=Depends(get_db_connection)):
    try:
        events = get_events(db)
        return events
    except Exception as e:
        # TODO - logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error retrieving events")


@api_router.get("/get/{event_code}", response_model=EventSummary)
def get_event(event_code: str, db=Depends(get_db_connection)):
    try:
        event_code = event_code.upper()
        event = get_event_by_code(db, event_code)
        return event
    except Exception as e:
        # TODO - logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error retrieving event")


@api_router.put("/update/{event_code}", response_model=MessageResponse)
def update_event_details(event_code: str, event_update: EventBase, db=Depends(get_db_connection)):
    try:
        event_code = event_code.upper()
        event_data_to_update = {
            k: v for k, v in event_update.model_dump().items() if v is not None}
        update_event(db, event_code, event_data_to_update)
        return {"message": "Event updated successfully"}
    except Exception as e:
        # TODO - logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error updating event")


@api_router.delete("/delete/{event_code}", response_model=MessageResponse)
def delete_event_by_code(event_code: str, db=Depends(get_db_connection)):
    try:
        event_code = event_code.upper()
        delete_event(db, event_code)
        return {"message": "Event deleted successfully"}
    except Exception as e:
        # TODO - logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error deleting event")
