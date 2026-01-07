from collections import Counter, defaultdict
from typing import Dict, List

def round_win_conditions(series_states: List[dict], team_name: str) -> Dict[str, float]:
    """
    Breakdown of win conditions (objective vs elimination) for a team.
    Percentages are based on total rounds won.
    """
    counts = Counter()

    for series in series_states:
        for game in series.get("games", []):
            for segment in game.get("segments", []):
                for team in segment.get("teams", []):
                    if team.get("name") != team_name or not team.get("won"):
                        continue

                    counts["total_wins"] += 1

                    objective_types = {obj["type"] for obj in team.get("objectives", [])}

                    if {"explodeBomb", "defuseBomb"} & objective_types:
                        counts["objective_wins"] += 1
                    else:
                        counts["elimination_wins"] += 1

    if counts["total_wins"] == 0:
        return {}

    total = counts["total_wins"]

    return {
        "total_wins": total,
        "objective_win_rate": (counts["objective_wins"] / total) * 100,
        "elimination_win_rate": (counts["elimination_wins"] / total) * 100,
    }


def win_condition_by_map(series_states: List[dict], team_name: str) -> Dict[str, dict]:
    """
    Win condition percentages per map for a given team.
    """
    stats = defaultdict(lambda: {
        "total_wins": 0,
        "objective_wins": 0,
        "elimination_wins": 0,
    })

    for series in series_states:
        for game in series.get("games", []):
            map_name = game["map"]["name"]

            for segment in game.get("segments", []):
                for team in segment.get("teams", []):
                    if team.get("name") != team_name or not team.get("won"):
                        continue

                    stats[map_name]["total_wins"] += 1

                    objective_types = {obj["type"] for obj in team.get("objectives", [])}

                    if {"explodeBomb", "defuseBomb"} & objective_types:
                        stats[map_name]["objective_wins"] += 1
                    else:
                        stats[map_name]["elimination_wins"] += 1

    results = {}

    for map_name, s in stats.items():
        total = s["total_wins"]
        if total == 0:
            continue

        results[map_name] = {
            "total_wins": total,
            "objective_win_rate": (s["objective_wins"] / total) * 100,
            "elimination_win_rate": (s["elimination_wins"] / total) * 100,
        }

    return results