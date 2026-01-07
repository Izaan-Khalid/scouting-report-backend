from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"

GRAPHQL_URL = "https://api-op.grid.gg/central-data/graphql"
LIVE_GRAPHQL_URL = "https://api-op.grid.gg/live-data-feed/series-state/graphql"

GRID_API_KEY = os.getenv("GRID_API_KEY")

HEADERS = {"x-api-key": GRID_API_KEY}

# Game title IDs GRID uses to identify different games
GAME_TITLES = {"VALORANT": "6", "LEAGUE_OF_LEGENDS": "3"}


# Map Win %
# Agent Win %
