from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from app.database.connection import get_db_connection
from app.schemas.models import MessageResponse, SessionCreate, SessionSummary, SessionUpdate
from app.utils.sessions import (
    add_session,
    delete_session,
    get_all_sessions,
    get_session_by_id,
    get_sessions_by_event,
    update_session,
)
from app.core.settings import logger

api_router = APIRouter(prefix="/sessions", tags=["sessions"])


@api_router.post("/create", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session: SessionCreate,
    background_tasks: BackgroundTasks,
    db=Depends(get_db_connection),
):
    """Create a new session."""
    try:
        return await add_session(db, session, background_tasks)
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.get("/list/{event_code}")
async def list_sessions(event_code: str, db=Depends(get_db_connection)):
    """List all sessions for an event, with nested speaker/track/venue details."""
    try:
        return await get_sessions_by_event(db, event_code)
    except Exception as e:
        logger.error(f"Error listing sessions for {event_code}: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.get("/list", response_model=list[SessionSummary])
async def list_all_sessions(db=Depends(get_db_connection)):
    """List all sessions across all events (admin)."""
    try:
        return await get_all_sessions(db)
    except Exception as e:
        logger.error(f"Error listing all sessions: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.get("/{session_id}", response_model=SessionSummary)
async def get_session(session_id: str, db=Depends(get_db_connection)):
    """Retrieve a session by its ID."""
    try:
        return await get_session_by_id(db, session_id)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.put("/update/{session_id}", response_model=MessageResponse)
async def update_session_details(
    session_id: str,
    session_update: SessionUpdate,
    background_tasks: BackgroundTasks,
    db=Depends(get_db_connection),
):
    """Update an existing session."""
    try:
        return await update_session(db, session_id, session_update, background_tasks)
    except Exception as e:
        logger.error(f"Error updating session {session_id}: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.delete("/delete/{session_id}", response_model=MessageResponse)
async def delete_session_by_id(
    session_id: str,
    background_tasks: BackgroundTasks,
    db=Depends(get_db_connection),
):
    """Delete a session by its ID."""
    try:
        return await delete_session(db, session_id, background_tasks)
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")
