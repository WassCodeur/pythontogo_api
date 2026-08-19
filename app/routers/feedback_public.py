from fastapi import APIRouter, BackgroundTasks, Request, status, HTTPException

from app.utils.feedback import add_feedback

from app.schemas.models import (
    FeedbackBase,
    MessageResponse,
)
from app.core.settings import logger


api_router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@api_router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def submit_public_feedback(request: Request, background_tasks: BackgroundTasks, payload: FeedbackBase):
    """Public endpoint to submit feedback without API key."""
    try:
        background_tasks.add_task(
            add_feedback, request.app.state.db_pool, payload.model_dump(mode="json"))
        return {"message": "Feedback received successfully"}
    except Exception as e:
        logger.error(f"Error adding public feedback: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail="Error adding feedback")
