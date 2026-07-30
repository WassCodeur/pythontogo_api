from uuid import uuid4

from fastapi import BackgroundTasks, HTTPException

from app.database.orm import delete, insert, select, select_with_join, update
from app.schemas.models import SessionCreate, SessionUpdate
from app.core.settings import logger
from app.utils.helpers import remove_null_values

SESSION_COLUMNS = [
    "sessions.id",
    "sessions.event_id",
    "sessions.venue_id",
    "sessions.track_id",
    "sessions.speaker_id",
    "sessions.title",
    "sessions.slug",
    "sessions.session_type",
    "sessions.starts_at",
    "sessions.ends_at",
    "sessions.description",
    "sessions.created_at",
    "sessions.updated_at",
]


async def get_all_sessions(db):
    try:
        sessions = await select(db, "sessions")
        if not sessions:
            raise HTTPException(status_code=404, detail="No sessions found")
        return sessions
    except Exception as e:
        logger.error(f"Error retrieving sessions: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_session_by_id(db, session_id: str):
    try:
        session = await select(db, "sessions", filter={"id": session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session[0]
    except Exception as e:
        logger.error(f"Error retrieving session {session_id}: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_sessions_by_event(db, event_code: str):
    """
    Retrieve all sessions for an event, enriched with nested speaker/track/venue
    details needed to render a schedule page.

    The speaker/track/venue lookups are done as separate queries and merged in
    Python rather than through a single multi-table SQL JOIN, because
    generate_multiple_joins_query() has no column-aliasing support and several
    of these tables share column names (id, name, created_at...) that would
    silently collide once merged into one flat row by psycopg's dict_row.
    """
    try:
        event_code = event_code.strip().upper()

        sessions = await select_with_join(
            db,
            table="sessions",
            join_table="events",
            join_condition="sessions.event_id = events.id",
            columns=SESSION_COLUMNS,
            filter={"events.code": event_code},
        )
        if not sessions:
            return []

        event_id = sessions[0]["event_id"]

        speakers = await select(db, "speakers", filter={"event_id": event_id})
        tracks = await select(db, "tracks", filter={"event_id": event_id})
        venues = await select(db, "venues", filter={"event_id": event_id})

        speakers_by_id = {row["id"]: row for row in (speakers or [])}
        tracks_by_id = {row["id"]: row for row in (tracks or [])}
        venues_by_id = {row["id"]: row for row in (venues or [])}

        for session in sessions:
            session["speaker"] = speakers_by_id.get(session.get("speaker_id"))
            session["track"] = tracks_by_id.get(session.get("track_id"))
            session["venue"] = venues_by_id.get(session.get("venue_id"))

        return sorted(sessions, key=lambda session: session["starts_at"])
    except Exception as e:
        logger.error(
            f"Error retrieving sessions for event {event_code}: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def add_session(db, session: SessionCreate, background_tasks: BackgroundTasks):
    try:
        session_data = session.model_dump(mode="json")
        session_data["id"] = str(uuid4())
        background_tasks.add_task(insert, db, "sessions", session_data)
        return {"message": "Session created successfully"}
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def update_session(db, session_id: str, session_update: SessionUpdate, background_tasks: BackgroundTasks):
    try:
        update_data = remove_null_values(
            session_update.model_dump(mode="json"))
        if not update_data:
            raise HTTPException(
                status_code=400, detail="No valid fields provided for update")

        existing = await select(db, "sessions", filter={"id": session_id})
        if not existing:
            raise HTTPException(status_code=404, detail="Session not found")

        background_tasks.add_task(
            update, db, "sessions", update_data, filter={"id": session_id})
        return {"message": "Session updated successfully"}
    except Exception as e:
        logger.error(f"Error updating session {session_id}: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")


async def delete_session(db, session_id: str, background_tasks: BackgroundTasks):
    try:
        existing = await select(db, "sessions", filter={"id": session_id})
        if not existing:
            raise HTTPException(status_code=404, detail="Session not found")

        background_tasks.add_task(
            delete, db, "sessions", filter={"id": session_id})
        return {"message": "Session deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")
