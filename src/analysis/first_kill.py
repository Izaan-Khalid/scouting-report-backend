from collections import Counter, defaultdict
from typing import Dict, List

def team_got_first_kill(round_events, team_name):
    """
    Returns True if team_name got the first kill in the round.
    """
    kill_events = [
        e for e in round_events
        if e.get("type") == "kill"
    ]

    if not kill_events:
        return False  # no kills in round

    first_kill = min(kill_events, key=lambda e: e["time"])
    return first_kill["killer"]["team"]["name"] == team_name


def first_kill_win_rate(series_states: List[dict], team_name: str) -> float:
    """
    Percentage of rounds won by a team after securing first kill.
    """
    first_kills = 0
    wins_after_first_kill = 0

    for series in series_states:
        for game in series.get("games", []):
            for segment in game.get("segments", []):
                for team in segment.get("teams", []):
                    if team.get("name") != team_name or not team.get("firstKill"):
                        continue

                    first_kills += 1
                    if team.get("won"):
                        wins_after_first_kill += 1

    if first_kills == 0:
        return 0.0

    return (wins_after_first_kill / first_kills) * 100

from collections import defaultdict

from collections import defaultdict

def first_kill_percentage_by_map(series_states, team_name):
    """
    Returns the % of rounds where team_name got first kill per map.
    """
    stats = defaultdict(lambda: {"first_kills": 0, "rounds": 0})

    for series in series_states:
        for game in series.get("games", []):
            map_name = game["map"]["name"]

            for segment in game.get("segments", []):
                stats[map_name]["rounds"] += 1

                # Use the existing firstKill boolean
                for team in segment.get("teams", []):
                    if team.get("name") == team_name and team.get("firstKill"):
                        stats[map_name]["first_kills"] += 1

    # Convert to percentages
    results = {}
    for map_name, data in stats.items():
        rounds = data["rounds"]
        results[map_name] = {
            "first_kill_percentage": (data["first_kills"] / rounds) * 100,
            "first_kills": data["first_kills"],
            "rounds_played": rounds,
        }

    return results

from collections import defaultdict

def map_level_first_kill_win(series_states, team_name):
    """
    For each map, calculate:
        - total rounds played
        - rounds with first kill
        - rounds won after first kill
        - first kill percentage
        - first kill → round win percentage
    """
    stats = defaultdict(lambda: {
        "total_rounds": 0,
        "first_kills": 0,
        "wins_after_first_kill": 0,
    })

    for series in series_states:
        for game in series.get("games", []):
            map_name = game["map"]["name"]

            for segment in game.get("segments", []):
                stats[map_name]["total_rounds"] += 1

                # find the team entry for our team
                team_data = next(
                    (t for t in segment.get("teams", []) if t.get("name") == team_name),
                    None
                )
                if not team_data:
                    continue

                if team_data.get("firstKill"):
                    stats[map_name]["first_kills"] += 1
                    if team_data.get("won"):
                        stats[map_name]["wins_after_first_kill"] += 1

    # Compute percentages
    results = {}
    for map_name, s in stats.items():
        first_kill_pct = (s["first_kills"] / s["total_rounds"]) * 100 if s["total_rounds"] else 0
        fk_win_pct = (s["wins_after_first_kill"] / s["first_kills"]) * 100 if s["first_kills"] else 0

        results[map_name] = {
            "total_rounds": s["total_rounds"],
            "first_kills": s["first_kills"],
            "wins_after_first_kill": s["wins_after_first_kill"],
            "first_kill_pct": first_kill_pct,
            "first_kill_to_win_pct": fk_win_pct,
        }

    return results


