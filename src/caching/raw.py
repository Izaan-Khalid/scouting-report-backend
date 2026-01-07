# src/storage/raw.py
from datetime import datetime, UTC
import json
from src.config.config import RAW_DIR

def cache_raw_series(team_id, edges, limit):
    payload = {
        "meta": {
            "source": "grid.gg",
            "endpoint": "allSeries",
            "team_id": team_id,
            "limit": limit,
            "fetched_at": datetime.now(UTC).isoformat()
        },
        "data": edges
    }

    path = RAW_DIR / "series" / f"{team_id}_series.json"
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
