import os
import json
from config import DATA_DIR

CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_cached_series(series_id: str) -> dict | None:
    cache_file = CACHE_DIR / f"series_state_{series_id}.json"
    if cache_file.exists():
        with open(cache_file, "r") as f:
            return json.load(f)
    return None

def cache_series_state(series_id: str, data: dict) -> None:
    cache_file = CACHE_DIR / f"series_state_{series_id}.json"
    with open(cache_file, "w") as f:
        json.dump(data, f, indent=2)