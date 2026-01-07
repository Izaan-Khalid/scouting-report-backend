from fetch.team import fetch_teams
from caching.team_lookup import load_team_cache, update_and_save_teams

def get_all_teams():
    cache = load_team_cache()
    return cache["VALORANT"]

def get_team_id(team_name: str, title_id: str) -> str:
    """
    Orchestrates getting a team ID: checks cache, then API, then updates cache.
    """
    cache = load_team_cache()
    team_name_lowered = team_name.strip().lower()

    title_name = ""
    if title_id == "1":
        title_id = "3"  # LoL
        title_name = "League of Legends"
    else:
        title_id = "6"  # Valorant
        title_name = "VALORANT"

    # Check cache (case-insensitive check is safer)
    # We look for an exact match first
    print(f"Checking cache for team '{team_name_lowered}'...")
    if title_name in cache and team_name_lowered in cache[title_name]:
        return cache[title_name][team_name_lowered], team_name

    # If not in cache, fetch from GRID
    print(f"Team '{team_name_lowered}' not found in cache. Fetching from GRID...")
    teams_list = fetch_teams(team_name_lowered, title_id)  # Returns [(id, name), ...]

    if not teams_list:
        raise ValueError(f"Team '{team_name_lowered}' could not be found via GRID API.")

    # 3. Update the cache with all results found (saves future API calls for variants)
    updated_cache = update_and_save_teams(teams_list, title_name)
    print(updated_cache)

    # 4. Return the specific ID requested
    # If the user searched 'Cloud9', we look for that exact key in the updated cache
    if team_name_lowered in updated_cache:
        return updated_cache[team_name_lowered], team_name

    # Fallback: If no exact match, return the first result from the API call
    # (e.g., if they searched 'C9' and GRID returned 'Cloud9')
    first_team = teams_list[0]
    first_id = first_team[0]
    first_name = first_team[1]

    print(f"Exact match not found. Defaulting to: {first_name} ({first_id})")
    return first_id, first_name

if __name__ == "__main__":
    get_team_id("KRU", "2")