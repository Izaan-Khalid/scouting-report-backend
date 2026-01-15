def generate_insight(report: dict) -> list[str]:
    """Generate actionable insights from the report data"""
    insights = []

    ov = report["overall"]

    # Win rate insight
    if ov["wins"] / ov["total_games"] > 0.65:
        insights.append(
            f"⚠️ High-performing team with {round((ov['wins'] / ov['total_games']) * 100, 1)}% win rate. Expect strong fundamentals.")
    elif ov["wins"] / ov["total_games"] < 0.40:
        insights.append(
            f"💡 Struggling team with {round((ov['wins'] / ov['total_games']) * 100, 1)}% win rate. Look for mistakes to punish.")

    # Map pool insights
    maps = report["maps"]
    best_map = max(maps.items(), key=lambda x: x[1]["wins"] / x[1]["total_games"] if x[1]["total_games"] > 0 else 0)
    worst_map = min(maps.items(), key=lambda x: x[1]["wins"] / x[1]["total_games"] if x[1]["total_games"] > 1 else 1)

    if best_map[1]["total_games"] > 2:
        best_wr = (best_map[1]["wins"] / best_map[1]["total_games"]) * 100
        insights.append(f"🎯 Dominant on {best_map[0].upper()} ({round(best_wr, 1)}% WR). Consider banning this map.")

    if worst_map[1]["total_games"] > 2:
        worst_wr = (worst_map[1]["wins"] / worst_map[1]["total_games"]) * 100
        if worst_wr < 40:
            insights.append(
                f"🎯 Vulnerable on {worst_map[0].upper()} ({round(worst_wr, 1)}% WR). Force them to play this map.")

    # Composition insights
    for map_name, data in maps.items():
        if data["total_games"] > 2:
            most_played_comp = max(data["comps"].items(), key=lambda x: x[1])
            comp_rate = (most_played_comp[1] / data["total_games"]) * 100
            if comp_rate > 60:
                insights.append(
                    f"📋 Predictable on {map_name.upper()}: {most_played_comp[0]} ({most_played_comp[1]} times, {round(comp_rate, 1)}%). Prepare specific counters.")

    # Draft insights
    draft = report["draft"]
    if draft["map_picks"]:
        most_picked = max(draft["map_picks"].items(), key=lambda x: x[1])
        insights.append(
            f"🗺️ Comfort pick: {most_picked[0].upper()} (picked {most_picked[1]} times). Expect them to pick this.")

    if draft["map_bans"]:
        most_banned = max(draft["map_bans"].items(), key=lambda x: x[1])
        insights.append(f"🚫 Weak on: {most_banned[0].upper()} (banned {most_banned[1]} times). They avoid this map.")

    return insights[:8]  # Return top 8 insights