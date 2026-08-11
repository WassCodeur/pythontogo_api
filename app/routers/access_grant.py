from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from app.schemas.grant import GrantSubmissionFormData
from app.utils.access_grant import create_access_grant

api_router = APIRouter(
    prefix="/access-grants", tags=["access-grant"])


@api_router.post("/{event_code}")
async def submit_grant_request(request: Request, event_code: str, form_data: GrantSubmissionFormData, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        create_access_grant, request.app.state.db_pool, form_data.model_dump(mode="json"), event_code.upper())

    return {"message": "Grant request submitted successfully."}
