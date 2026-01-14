from fastapi import APIRouter, HTTPException
from services.matchup_service import get_head_to_head
from services.team_service import get_all_teams

router = APIRouter()

@router.get("/{team_a_id}/vs/{team_b_id}")
def matchups(team_a_id: str, team_b_id: str):
    teams = get_all_teams()

    # Get team names
    team_a_name = next((name for name, tid in teams.items() if tid == team_a_id), None)
    team_b_name = next((name for name, tid in teams.items() if tid == team_b_id), None)

    if not team_a_name or not team_b_name:
        raise HTTPException(status_code=404, detail="Invalid team ID")

    matchup = get_head_to_head(team_a_id, team_b_id)

    return {
        "team_a": {"id": team_a_id, "name": team_a_name},
        "team_b": {"id": team_b_id, "name": team_b_name},
        **matchup
    }
