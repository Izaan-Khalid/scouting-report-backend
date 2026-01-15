def generate_insight(report: dict) -> dict:
    """Generate actionable insights from the report data"""
    insights = {
        "map_pool": [],
        "strategy": [],
        "composition": [],
    }

    ov = report["overall"]

    # Win rate insight
    if ov["wins"] / ov["total_games"] > 0.65:
        insights["strategy"].append(
            f"⚠️ High-performing team with {round((ov['wins'] / ov['total_games']) * 100, 1)}% win rate. Expect strong fundamentals.")
    elif ov["wins"] / ov["total_games"] < 0.40:
        insights["strategy"].append(
            f"💡 Struggling team with {round((ov['wins'] / ov['total_games']) * 100, 1)}% win rate. Look for mistakes to punish.")

    # First blood insights
    fb_wr = ov["fk_wins"] / ov["fk_total"] if ov["fk_total"] > 0 else 0
    if fb_wr > 0.70:
        insights["strategy"].append(
            f"Strong first blood conversion rate ({round(fb_wr * 100, 1)}%). Avoid giving them early picks - they snowball rounds effectively.")
    elif fb_wr < 0.50:
        insights["strategy"].append(
            f"Weak first blood conversion ({round(fb_wr * 100, 1)}%). Getting first blood doesn't guarantee round wins. Stay patient and play for late-round.")

    # Map pool insights
    maps = report["maps"]
    map_records = [(name, data) for name, data in maps.items()]
    map_records.sort(key=lambda x: x[1]["wins"] / x[1]["total_games"] if x[1]["total_games"] > 0 else 0,
                     reverse=True)

    # Best maps
    for map_name, data in map_records[:2]:
        if data["total_games"] > 2:
            wr = (data["wins"] / data["total_games"]) * 100
            if wr > 60:
                insights["map_pool"].append(
                    f"Dominant on {map_name.upper()} ({round(wr, 1)}% WR, {data['wins']}-{data['total_games'] - data['wins']}). High-priority ban target.")

    # Worst maps
    for map_name, data in map_records[-2:]:
        if data["total_games"] > 2:
            wr = (data["wins"] / data["total_games"]) * 100
            if wr < 40:
                insights["map_pool"].append(
                    f"Vulnerable on {map_name.upper()} ({round(wr, 1)}% WR, {data['wins']}-{data['total_games'] - data['wins']}). Force them to play this map.")

    # Composition insights
    for map_name, data in maps.items():
        if data["total_games"] > 2:
            most_played_comp = max(data["comps"].items(), key=lambda x: x[1])
            comp_rate = (most_played_comp[1] / data["total_games"]) * 100
            if comp_rate > 60:
                insights["compositions"].append(
                    f"Predictable on {map_name.upper()}: {most_played_comp[0]} ({most_played_comp[1]}/{data['total_games']} games, {round(comp_rate, 1)}%). Prepare agent-specific counters.")

    # Draft insights
    draft = report["draft"]
    if draft["map_picks"]:
        picks_sorted = sorted(draft["map_picks"].items(), key=lambda x: x[1], reverse=True)
        if picks_sorted[0][1] > 1:
            insights["map_pool"].append(
                f"Comfort pick: {picks_sorted[0][0].upper()} (selected {picks_sorted[0][1]} times). Expect them to pick this in draft.")

    if draft["map_bans"]:
        bans_sorted = sorted(draft["map_bans"].items(), key=lambda x: x[1], reverse=True)
        if bans_sorted[0][1] > 2:
            insights["map_pool"].append(
                f"Consistently bans {bans_sorted[0][0].upper()} ({bans_sorted[0][1]} times). Clear weakness - leave it open to force a ban or make them play it.")

    return insights