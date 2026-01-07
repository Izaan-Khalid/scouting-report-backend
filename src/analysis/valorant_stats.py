from collections import defaultdict


def calculate_all_metrics(series_states: list, team_id: str) -> dict:
    """
    Calculate various Valorant statistics for a given team.
    """
    metrics = {
        "overall": {"wins": 0, "total_games": 0, "fk_wins": 0, "fk_total": 0},
        "draft": {
            "map_picks": defaultdict(int),
            "map_bans": defaultdict(int),
            "pick_order": defaultdict(list),
            "ban_order": defaultdict(list),
        },
        "maps": defaultdict(
            lambda: {
                "wins": 0,
                "total_games": 0,
                "fk_wins": 0,
                "fk_total": 0,
                "comps": defaultdict(int),
                "win_conditions": defaultdict(int),
            }
        ),
    }

    for series in series_states:
        pick_idx = 0
        ban_idx = 0
        for draft in series.get("draftActions", []):
            if draft["drafter"]["id"] != team_id:
                continue

            map_name = draft["draftable"]["name"]

            if draft["type"] == "pick":
                pick_idx += 1
                metrics["draft"]["map_picks"][map_name] += 1
                metrics["draft"]["pick_order"][map_name].append(pick_idx)

            elif draft["type"] == "ban":
                ban_idx += 1
                metrics["draft"]["map_bans"][map_name] += 1
                metrics["draft"]["ban_order"][map_name].append(ban_idx)

        for game in series.get("games", []):
            map_name = game["map"]["name"]
            metrics["overall"]["total_games"] += 1
            metrics["maps"][map_name]["total_games"] += 1

            # Identify team
            us = next((t for t in game["teams"] if t["id"] == team_id), None)
            if not us:
                continue

            # Map wins
            if us["won"]:
                metrics["overall"]["wins"] += 1
                metrics["maps"][map_name]["wins"] += 1

            # Agent composition (sorted)
            agents = sorted([p["character"]["name"] for p in us["players"]])
            comp_str = ", ".join(agents)
            metrics["maps"][map_name]["comps"][comp_str] += 1

            # Round-by-Round Analysis (First Bloods & Win Conditions)
            for segment in game.get("segments", []):
                # Filter segments for us
                team_segment = next(
                    (t for t in segment["teams"] if t["id"] == team_id), None
                )
                if not team_segment:
                    continue

                # First Blood Metrics
                if team_segment.get("firstKill"):
                    metrics["overall"]["fk_total"] += 1
                    metrics["maps"][map_name]["fk_total"] += 1
                    if team_segment.get("won"):
                        metrics["overall"]["fk_wins"] += 1
                        metrics["maps"][map_name]["fk_wins"] += 1

                # Win Condition Metrics
                if team_segment.get("won"):
                    condition = "Elimination"
                    for obj in team_segment.get("objectives", []):
                        if obj["type"] in {"explodeBomb", "defuseBomb"}:
                            condition = "Objective"
                    metrics["maps"][map_name]["win_conditions"][condition] += 1

    return metrics