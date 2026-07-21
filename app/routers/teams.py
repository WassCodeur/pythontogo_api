from fastapi import APIRouter, Depends, HTTPException
from app.schemas.teams import TeamCreate, TeamUpdate, TeamMemberResponse
from app.utils.teams import create_team, get_team_by_event_code
from app.database.connection import get_db_connection


api_router = APIRouter(prefix="/teams", tags=["Teams"])


@api_router.get("/{event_code}")
async def get_teams(event_code: str, db=Depends(get_db_connection)):
    return await get_team_by_event_code(db, event_code.upper())


@api_router.post("/{event_code}")
async def create_team_member(event_code: str, team_data: TeamCreate, db=Depends(get_db_connection)):
    team_data_dict = team_data.model_dump()
    try:
        return await create_team(db, team_data_dict, event_code.upper())
    except Exception as e:
        import traceback
        traceback.print_exc()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail=str(e))


@api_router.post('/addmany/{event_code}')
async def create_multiple_team_members(event_code: str, team_members: list[TeamCreate], db=Depends(get_db_connection)):
    for team_data in team_members:

        team_data.email = f"{team_data.full_name[0].lower()}.{team_data.full_name.split(' ')[-1].lower()}@pytogo.org"
        team_data_dict = team_data.model_dump(mode="json")
        try:
            await create_team(db, team_data_dict, event_code.upper())
        except Exception as e:
            import traceback
            traceback.print_exc()
    return {"created_members": len(team_members)}
