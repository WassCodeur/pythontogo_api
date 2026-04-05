from app.database.orm import select, insert, update, select_with_join, delete


async def add_contact(db, payload: dict):
    try:
        await insert(db, "contacts", payload)
    except Exception as e:
        # TODO logging the error can be done here
        pass


async def delete_contact(db, contact_id: str):
    try:
        await delete(db, "contacts", filter={"id": contact_id})
    except Exception as e:
        # TODO logging the error can be done here
        pass


async def get_contact_by_id(db, contact_id: str):
    try:
        contact = await select(db, "contacts", filter={"id": contact_id})
        if not contact:
            # TODO logging the error can be done here
            pass
        return contact[0]
    except Exception as e:
        # TODO logging the error can be done here
        pass


async def get_contacts_by_event(db, event_code: str):
    try:
        contacts = await select_with_join(
            db,
            table="contacts",
            join_table="events",
            join_condition="contacts.event_id = events.id",
            filter={"events.code": event_code},
        )
        return contacts
    except Exception as e:
        # TODO logging the error can be done here
        pass


async def get_all_contacts(db):
    try:
        contacts = await select(db, "contacts")
        return contacts
    except Exception as e:
        # TODO logging the error can be done here
        pass


async def update_contact(db, contact_id: str, payload: dict):
    try:
        existing = await select(db, "contacts", filter={"id": contact_id})
        if not existing:
            # TODO logging the error can be done here
            pass
        await update(db, "contacts", payload, filter={"id": contact_id})
    except Exception as e:
        # TODO logging the error can be done here
        pass
