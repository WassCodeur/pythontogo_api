from app.database.orm import select, insert, update, select_with_join, delete
from uuid import uuid4
from fastapi import HTTPException, status


async def add_sponsor_partner(db, payload: dict, event_code: str):
    try:
        existing = await select_with_join(
            db,
            table="sponsors_partners",
            join_table="events",
            join_condition="sponsors_partners.event_id = events.id",
            filter={"events.code": event_code,
                    "sponsors_partners.name": payload["name"]},
        )

        if existing:
            # TODO: sent email to admin about duplicate request
            pass
        event = await select(db, "events", filter={"year": payload["edition_year"]})
        if not event:
            pass

        payload.update({
            "id": str(uuid4()),
            "event_id": event[0]["id"],
        })
        await insert(db, "sponsors_partners", payload)

    except Exception as e:
        # logging the error can be done here
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error adding sponsor/partner")


async def _update_partner_sponsor(db, partner_id: str, payload: dict):
    try:
        existing = await select(db, "sponsors_partners", filter={"id": partner_id})
        if not existing:
            # TODO - logging the error can be done here
            pass
        await update(db, "sponsors_partners", payload, filter={"id": partner_id})

    except Exception as e:
        # TODO - logging the error can be done here
        pass


async def get_sponsors_partners_by_event(db, event_code: str):
    try:
        partners = await select_with_join(
            db,
            table="sponsors_partners",
            join_table="events",
            join_condition="sponsors_partners.event_id = events.id",
            filter={"events.code": event_code},
        )
        if not partners:
            # TODO - logging the error can be done here
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No sponsors/partners found for event code {event_code}")
        return partners
    except Exception as e:
        # TODO - logging the error can be done here
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error fetching sponsors/partners")


async def get_sponsors_partners(db):
    try:
        partners = await select(db, "sponsors_partners")
        return partners
    except Exception as e:
        # TODO - logging the error can be done here
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error fetching sponsors/partners")


async def delete_sponsor_partner(db, partner_id: str):
    try:
        existing = await select(db, "sponsors_partners", filter={"id": partner_id})
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Sponsor/Partner not found")
        await delete(db, "sponsors_partners", filter={"id": partner_id})

    except Exception as e:
        # TODO - logging the error can be done here
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error deleting sponsor/partner")
