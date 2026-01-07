import requests
from config import LIVE_GRAPHQL_URL, HEADERS


SERIES_STATE_QUERY = """
query GetSeriesState($seriesId: ID!) {
    seriesState(id: $seriesId) {
        id
        updatedAt
        format
        draftActions {
            id
            type
            sequenceNumber
            drafter {
                id
            }
            draftable{
                name
            }
        }
        teams {
            id
            name
            won
            score
        }
        games {
            map {
                name
            }
            sequenceNumber
            teams {
                id
                name
                score
                won
                kills
                deaths
                players {
                    name
                    character {
                        name
                    }
                    kills
                    deaths
                }
            }
            segments {
                id
                teams {
                    id
                    name
                    side
                    won
                    kills
                    deaths
                    firstKill
                    objectives{
                        id
                        type
                    }
                }
            } 
        }
    }
}
"""


def fetch_serie_state(series_id: str) -> dict:
    """
    Fetches the state of a single series.
    """
    state = {}

    print(f"Fetching state for {series_id}...")

    payload = {"query": SERIES_STATE_QUERY, "variables": {"seriesId": series_id}}

    try:
        r = requests.post(LIVE_GRAPHQL_URL, headers=HEADERS, json=payload)
        r.raise_for_status()

        data = r.json()
        series_state = data["data"]["seriesState"]
        if data:
            state = series_state
            print(f" ✅ Successfully fetched ID: {series_id}")
        else:
            print(f" ⚠️ No data found for ID: {series_id}")
    except requests.RequestException as e:
        print(f"Error fetching series state for ID {series_id}: {e}")

    return state
