from fastapi import APIRouter, BackgroundTasks, Depends, status, HTTPException

from app.utils.contact import (
    add_contact, get_contacts_by_event, get_contact_by_id, get_all_contacts, update_contact, delete_contact)

from app.schemas.models import (
    MessageResponse,
    ContactMessageUpdate,
    ContactBase,
    ContactMessagesList,

)
from app.database.connection import get_db_connection


api_router = APIRouter(prefix="/contacts", tags=["contacts"])


@api_router.get("/{event_code}", response_model=ContactMessagesList)
async def get_contacts(event_code: str, db=Depends(get_db_connection)):
    try:
        event_code = event_code.upper()
        contacts = await get_contacts_by_event(db, event_code)
        return contacts
    except Exception as e:
        # TODO - logging the error can be done here
        raise HTTPException(
            status_code=500, detail="Error retrieving contacts")


@api_router.get("/", response_model=ContactMessagesList)
async def _get_all_contacts(db=Depends(get_db_connection)):
    try:
        contacts = await get_all_contacts(db)
        return contacts
    except Exception as e:
        # TODO - logging the error can be done here
        raise HTTPException(
            status_code=500, detail="Error retrieving contacts")


@api_router.get("/{contact_id}", response_model=ContactBase)
async def _get_contact_by_id(contact_id: str, db=Depends(get_db_connection)):
    try:
        contact = await get_contact_by_id(db, contact_id)
        if not contact:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Contact with id {contact_id} not found")
        return contact
    except Exception as e:
        # TODO - logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail="Error retrieving contact")


@api_router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def add_contact_message(payload: ContactBase, background_tasks: BackgroundTasks, db=Depends(get_db_connection)):
    try:
        background_tasks.add_task(add_contact, db, payload.model_dump())
        return {"message": "Contact message added successfully"}
    except Exception as e:
        # TODO - logging the error can be done here
        raise HTTPException(
            status_code=500, detail="Error adding contact message")


@api_router.post("/{event_code}", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def add_contact_message(event_code: str, payload: ContactBase, background_tasks: BackgroundTasks, db=Depends(get_db_connection)):
    try:
        event_code = event_code.upper()
        payload_dict = payload.model_dump()
        payload_dict.update({"event_code": event_code})
        background_tasks.add_task(add_contact, db, payload_dict)
        return {"message": "Contact message added successfully"}
    except Exception as e:
        # TODO - logging the error can be done here
        raise HTTPException(
            status_code=500, detail="Error adding contact message")


@api_router.put("/{contact_id}", response_model=MessageResponse)
async def _update_contact(contact_id: str, payload: ContactMessageUpdate, background_tasks: BackgroundTasks, db=Depends(get_db_connection)):
    try:
        data_to_update = {k: v for k,
                          v in payload.model_dump().items() if v is not None}
        background_tasks.add_task(
            update_contact, db, contact_id, data_to_update)
        return {"message": "Contact updated successfully"}
    except Exception as e:
        # TODO - logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail="Error updating contact")


@api_router.delete("/{contact_id}", response_model=MessageResponse)
async def _delete_contact(contact_id: str, background_tasks: BackgroundTasks, db=Depends(get_db_connection)):
    try:
        background_tasks.add_task(delete_contact, db, contact_id)
        return {"message": "Contact deleted successfully"}
    except Exception as e:
        # TODO - logging the error can be done here
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail="Error deleting contact")
