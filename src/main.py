from collections import defaultdict

from services.team_service import get_team_id, get_all_teams
from fetch.series import fetch_recent_series_id
from services.serie_state_service import get_series_states
from analysis.valorant_stats import calculate_all_metrics

def to_dict(obj):
    if isinstance(obj, defaultdict):
        return {k: to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_dict(v) for v in obj]
    else:
        return obj


def run_scouting_report(team_name: str, game_id: str = "1"):
    print(f"\n🔍 Generating scouting report for {team_name}...\n")

    # Get Team ID
    team_id, team_name = get_team_id(team_name, game_id)

    if not team_id:
        print(f"❌ Team '{team_name}' not found.")
        return

    # Fetch Recent Series ID
    series_ids = fetch_recent_series_id(team_id)
    print(series_ids)

    # Get Series States
    series_states = get_series_states(series_ids)

    # Calculate Metrics
    report = calculate_all_metrics(series_states, team_id)
    clean_metrics = to_dict(report)

    # SECTION 1: OVERALL PERFORMANCE
    print(f"{'='*100}")
    print(f"🏆 SCOUTING REPORT FOR {team_name.upper()}")
    print(f"{'='*100}\n")
    ov = report["overall"]

    win_rate = (ov["wins"] / ov["total_games"]) * 100 if ov["total_games"] > 0 else 0
    fk_win_rate = (ov["fk_wins"] / ov["fk_total"]) * 100 if ov["fk_total"] > 0 else 0

    # OVERALL
    print(f"📊 OVERALL STATS")
    print(f"- Total Games Played: {ov['total_games']}")
    print(f"- Total Wins:         {ov['wins']}")
    print(f"- Series Win Rate:    {win_rate:.1f}%")
    print(f"- First Bloods:       {ov['fk_total']}")
    print(f"- FB to Win Count:    {ov['fk_wins']}")
    print(f"- FK → Round Win:     {fk_win_rate:.1f}%")
    print("-" * 30)


    # Sort maps by total games played (descending)
    sorted_maps = sorted(
        clean_metrics["maps"].items(),
        key=lambda x: x[1]["total_games"],  # sort by total_games
        reverse=True
    )

    # # MAP BREAKDOWN
    for map_name, data in sorted_maps:
        total_games = data["total_games"]
        wins = data["wins"]
        fk_total = data["fk_total"]
        fk_wins = data["fk_wins"]
        win_rate = (wins / total_games) * 100 if total_games > 0 else 0
        fk_win_rate = (fk_wins / fk_total) * 100 if fk_total > 0 else 0

        # All agent comps
        comps = data["comps"]
        if comps:
            comps_str = ", ".join([f"{k} ({v})" for k, v in comps.items()])
        else:
            comps_str = "N/A"

        # Win conditions
        win_conditions = ", ".join([f"{k} ({v})" for k, v in data["win_conditions"].items()])

        # Draft info
        draft_data = clean_metrics["draft"]
        picks = draft_data["map_picks"].get(map_name, 0)
        pick_order = draft_data["pick_order"].get(map_name, [])
        bans  = draft_data["map_bans"].get(map_name, 0)
        ban_order = draft_data["ban_order"].get(map_name, [])

        print(f"Map: {map_name.title()}")
        print(f"  Games Played: {total_games}")
        print(f"  Wins: {wins}")
        print(f"  Win Rate: {win_rate:.1f}%")
        print(f"  First Bloods: {fk_wins} / {fk_total} ({fk_win_rate:.1f}%)")
        print(f"  Agent Compositions: {comps_str}")
        print(f"  Win Conditions: {win_conditions}")
        print(f"  Draft Picks: {picks} | Pick Order: {pick_order}")
        print(f"  Draft Bans: {bans} | Ban Order: {ban_order}")
        print("-" * 100)

def build_report(team_id):
    series_ids = fetch_recent_series_id(team_id)
    series_states = get_series_states(series_ids)
    report = calculate_all_metrics(series_states, team_id)
    return to_dict(report)

def main():
    game_id = input("Enter the game ID (1 = League of Legends, 2 = Valorant): ").strip()
    if game_id not in ["1", "2"]:
        print(
            "❌ Invalid game ID. Please enter 1 for League of Legends or 2 for Valorant."
        )
        return

    team_lookup = get_all_teams()

    print("Available teams:")
    for team_name, team_id in team_lookup.items():
        print(f"- {team_name}: {team_id}")

    team_name = input("Enter the team name for scouting report: ").strip()
    if team_name not in team_lookup:
        print("❌ Invalid team name. Please choose from the list above.")
        return
    else:
        run_scouting_report(team_name, game_id)

def test_main():
    run_scouting_report("mibr", 2)

if __name__ == "__main__":
    main()
