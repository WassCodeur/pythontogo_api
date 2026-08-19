from fastapi import HTTPException, BackgroundTasks
from app.core.settings import logger

from app.database.orm import select, insert, update, delete


async def add_feedback(db, payload: dict):
    try:
        await insert(db, "feedbacks", payload)
        return {"message": "Feedback received successfully"}
    except Exception as e:
        logger.error(f"Error adding feedback: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail="Error adding feedback")


async def delete_feedback(db, feedback_id: str, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(
            delete, db, "feedbacks", filter={"id": feedback_id})
        return {"message": "Feedback deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting feedback: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Error deleting feedback")


async def get_feedback_by_id(db, feedback_id: str):
    try:
        feedback = await select(db, "feedbacks", filter={"id": feedback_id})
        if not feedback:
            logger.error(f"Feedback with id {feedback_id} not found")
        return feedback[0]
    except Exception as e:
        logger.error(f"Error retrieving feedback: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Error retrieving feedback")


async def get_all_feedbacks(db):
    try:
        feedbacks = await select(db, "feedbacks")
        return feedbacks
    except Exception as e:
        logger.error(f"Error retrieving all feedbacks: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail="Error retrieving all feedbacks")


async def update_feedback(db, feedback_id: str, payload: dict, background_tasks: BackgroundTasks):
    try:
        existing = await select(db, "feedbacks", filter={"id": feedback_id})
        if not existing:
            logger.error(f"Feedback with id {feedback_id} not found")
            raise HTTPException(
                status_code=404, detail=f"Feedback with id {feedback_id} not found")
        background_tasks.add_task(
            update, db, "feedbacks", payload, filter={"id": feedback_id})
        return {"message": "Feedback updated successfully"}
    except Exception as e:
        logger.error(f"Error updating feedback: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Error updating feedback")
