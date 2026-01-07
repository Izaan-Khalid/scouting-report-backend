import requests
from config import GRAPHQL_URL, HEADERS

GET_SERIES_BY_KEYS_QUERY = """
query GetSeriesKeys($teamIds: IdFilter) {
  allSeries(
    filter: { 
        teamIds: $teamIds, 
    }
    first: 10
    orderBy: StartTimeScheduled
    orderDirection: DESC
  ) {
    edges {
      node {
        id
        teams {
          baseInfo {
            id
            name
          }
        }
        startTimeScheduled
      }
    }
  }
}
"""


def fetch_recent_series_id(team_id: str) -> str | None:
    """
    Fetches the IDs of the 5 most recent finished matches for a team.
    """
    payload = {
        "query": GET_SERIES_BY_KEYS_QUERY,
        "variables": {"teamIds": {"in": [team_id]}},
    }

    try:
        r = requests.post(GRAPHQL_URL, headers=HEADERS, json=payload)
        r.raise_for_status()

        data = r.json()

        if "errors" in data:
            print(f"GraphQL Errors: {data['errors']}")
            return []

        if "data" not in data or data["data"] is None:
            print(f"Unexpected response structure: {data}")
            return []

        # Extract the IDs from the nested edges
        edges = data["data"].get("allSeries", {}).get("edges", [])
        series_id = [edge["node"]["id"] for edge in edges]

        return series_id

    except requests.RequestException as e:
        print(f"Error fetching recent series: {e}")
        return []

if __name__ == "__main__":
    test_id = "79"
    print(f"Testing get_serie_state for ID: {test_id}")
    state = fetch_recent_series_id(test_id)
    print(f"IDs: {state}")