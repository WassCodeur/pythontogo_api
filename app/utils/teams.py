from app.database.orm import select, insert, update, delete, select_with_join, select_with_multiple_joins
from app.core.settings import logger


async def create_team(db, team_data, event_code):
    try:
        event = await select(db, "events", filter={"code": event_code.upper()})
        member_exists = await select(db, "team_members", filter={"email": team_data["email"], "event_id": event[0]["id"]})
        if member_exists:
            raise Exception(
                "Team member with this email already exists for the event.")
        team_data["event_id"] = event[0]["id"]
        await insert(db, "team_members", team_data)
        return {"message": "Team member created successfully", "team_member_full_name": team_data["full_name"]}
    except Exception as e:
        logger.error(f"Error creating team: {str(e)}")
        raise


async def get_team_by_event_code(db, event_code):
    try:
        team_members = await select_with_join(
            db,
            "team_members",
            "events",
            "team_members.event_id = events.id",
            columns=["team_members.full_name", "team_members.role", "team_members.bio", "team_members.photo_url",
                     "team_members.social_links", "team_members.is_volunteer", "team_members.is_active", "team_members.position"],
            filter={"events.code": event_code}
        )
        return team_members if team_members else {}
    except Exception as e:
        logger.error(
            f"Error fetching team members for event code {event_code}: {str(e)}")
        raise
