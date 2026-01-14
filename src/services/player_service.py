from collections import defaultdict
from fetch.series import fetch_recent_series_id
from services.serie_state_service import get_series_states


def get_team_players(team_id: str) -> list[dict]:
    """Get aggregated player stats for a team"""
    series_ids = fetch_recent_series_id(team_id)
    series_states = get_series_states(series_ids)

    # Aggregare stats per player
    player_stats = defaultdict(lambda: {
        "kills": 0,
        "deaths": 0,
        "games": 0,
        "agents": defaultdict(int)
    })

    for state in series_states:
        for game in state.get("games", []):
            for team in game.get("teams", []):
                if team["id"] == team_id:
                    for player in team.get("players", []):
                        name = player["name"]
                        player_stats[name]["kills"] += player["kills"]
                        player_stats[name]["deaths"] += player["deaths"]
                        player_stats[name]["games"] += 1
                        player_stats[name]["agents"][player["character"]["name"]] += 1

        # Format output
    result = []
    for name, stats in player_stats.items():
        kd = round(stats["kills"] / stats["deaths"], 2) if stats["deaths"] > 0 else 0
        avg_kills = round(stats["kills"] / stats["games"], 1) if stats["games"] > 0 else 0

        # Get top 3 most played agents
        top_agents = sorted(stats["agents"].items(), key=lambda x: x[1], reverse=True)[:3]

        result.append({
            "name": name,
            "kd_ratio": kd,
            "avg_kills": avg_kills,
            "total_kills": stats["kills"],
            "total_deaths": stats["deaths"],
            "games_played": stats["games"],
            "top_agents": [
                {"agent": agent, "games": count}
                for agent, count in top_agents
            ]
        })

    # Sort by KD ratio
    result.sort(key=lambda x: x["kd_ratio"], reverse=True)
    return result

if __name__ == "__main__":
    print(get_team_players("79"))