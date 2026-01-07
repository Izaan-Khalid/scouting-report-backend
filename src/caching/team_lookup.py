import json
from pathlib import Path

from config import RAW_DIR

CACHE_PATH = RAW_DIR / "team_lookup.json"


def load_team_cache():
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}


def save_team_cache(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)


def update_and_save_teams(new_teams: list[tuple[str, str]], title_name: str) -> dict:
    """
    Takes the list of tuples from fetch_teams, merges it with existing
    cache, and saves to disk.
    """
    current_cache = load_team_cache()

    # Convert list of tuples (id, name) to dict {name: id}
    # Note: We use name as key for quick string-based lookups
    new_data = {name.lower(): team_id for team_id, name in new_teams}

    # Update current cache with new findings
    current_cache[title_name].update(new_data)

    save_team_cache(current_cache)
    print(f"Updated team cache: {current_cache}")
    return current_cache


def cache_team_lookup(teams):
    """
    Save the team ID lookup to a JSON file for reuse.
    """
    print("Caching team lookup...")
    path = RAW_DIR / "team_lookup.json"
    path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing cache if exists
    if path.exists():
        with open(path, "r") as f:
            cache = json.load(f)
    else:
        cache = {}

    for t in teams:
        team_id, team_name = t
        cache[team_name] = {"id": team_id, "name": team_name}

    print(f"Cache updated: ", cache)

    with open(path, "w") as f:
        json.dump(cache, f, indent=2)
