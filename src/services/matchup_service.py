from fetch.series import fetch_recent_series_id
from services.serie_state_service import get_series_states


def get_head_to_head(team_a_id: str, team_b_id: str) -> dict:
    """Get head-to-head stats for two teams"""

    # Get series for both teams
    series_a = set(fetch_recent_series_id(team_a_id))
    series_b = set(fetch_recent_series_id(team_b_id))

    # Find matches they played against each other
    common_series = series_a.intersection(series_b)

    if not common_series:
        return {
            "matches_played": 0,
            "message": "No matches found between these teams."
        }

    states = get_series_states(list(common_series))

    team_a_wins = 0
    team_b_wins = 0
    map_records = {}

    for state in states:
        # Check series winner
        for team in state.get("teams", []):
            if team["id"] == team_a_id and team.get("won"):
                team_a_wins += 1
            elif team["id"] == team_b_id and team.get("won"):
                team_b_wins += 1

        # Track map wins
        for game in state.get("games", []):
            map_name = game["map"]["name"]
            if map_name not in map_records:
                map_records[map_name] = {"team_a_wins": 0, "team_b_wins": 0}

            for team in game.get("teams", []):
                if team["id"] == team_a_id and team.get("won"):
                    map_records[map_name]["team_a_wins"] += 1
                elif team["id"] == team_b_id and team.get("won"):
                    map_records[map_name]["team_b_wins"] += 1

    return {
        "matches_played": len(common_series),
        "team_a_wins": team_a_wins,
        "team_b_wins": team_b_wins,
        "map_records": [
            {"map": map_name, **stats}
            for map_name, stats in map_records.items()
        ]
    }