from fastapi import APIRouter, HTTPException
from services.team_service import get_all_teams
from main import build_report
from services.player_service import get_team_players

router = APIRouter()

@router.get("")
def list_teams():
    teams = get_all_teams()
    return [{
        "id": tid, "name": name
    } for name, tid in teams.items()]

@router.get("/{team_id}/overall")
def team_overall(team_id: str):
    report = build_report(team_id)

    if not report:
        raise HTTPException(status_code=404, detail="Team not found")

    ov = report["overall"]

    # ---------- OVERVIEW ----------
    overview = {
        "total_games": ov["total_games"],
        "wins": ov["wins"],
        "win_rate": round(
            (ov["wins"] / ov["total_games"]) * 100
            if ov["total_games"] else 0, 2
        ),
        "first_bloods": ov["fk_total"],
        "first_blood_win_rate": round(
            (ov["fk_wins"] / ov["fk_total"]) * 100
            if ov["fk_total"] else 0, 2
        )
    }

    # ---------- MAPS ----------
    maps = []
    for map_name, data in report["maps"].items():
        maps.append({
            "name": map_name,
            "games": data["total_games"],
            "wins": data["wins"],
            "win_rate": round(
                (data["wins"] / data["total_games"]) * 100
                if data["total_games"] else 0, 2
            ),
            "first_blood_win_rate": round(
                (data["fk_wins"] / data["fk_total"]) * 100
                if data["fk_total"] else 0, 2
            ),
            "comps": [
                {"agents": agents, "count": count}
                for agents, count in data["comps"].items()
            ],
            "win_conditions": data["win_conditions"]
        })

    # Sort maps by most played
    maps.sort(key=lambda m: m["games"], reverse=True)

    # ---------- DRAFT ----------
    draft = {
        "picks": [
            {
                "map": map_name,
                "count": count,
                "order": report["draft"]["pick_order"].get(map_name, [])
            }
            for map_name, count in report["draft"]["map_picks"].items()
        ],
        "bans": [
            {
                "map": map_name,
                "count": count,
                "order": report["draft"]["ban_order"].get(map_name, [])
            }
            for map_name, count in report["draft"]["map_bans"].items()
        ]
    }

    return {
        "overview": overview,
        "maps": maps,
        "draft": draft
    }

@router.get("/{team_id}/players")
def team_players(team_id: str):
    players = get_team_players(team_id)
    if not players:
        raise HTTPException(status_code=404, detail="No player data found")
    return players