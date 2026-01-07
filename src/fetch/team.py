import requests
from config import GRAPHQL_URL, HEADERS

# GraphQL query to find a team by name
FIND_TEAM_QUERY = """
query FindTeam($name: StringFilter!, $titleId: ID!) {
  teams(first: 5, filter:
    { name: $name, titleId: $titleId }) {
    edges {
      node {
        id
        name
        titles {
          id
          name
        }
      }
    }
  }
}
"""


def fetch_teams(name: str, title_id: str) -> list[tuple[str, str]]:
    """
    Fetch team IDs from GRID by name (using StringFilter 'contains').
    Returns a list of tuples: (team_id, team_name)
    """
    payload = {
        "query": FIND_TEAM_QUERY,
        "variables": {"name": {"contains": name}, "titleId": title_id},
    }

    r = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
    r.raise_for_status()

    edges = r.json()["data"]["teams"]["edges"]
    team_list = [(edge["node"]["id"], edge["node"]["name"]) for edge in edges]
    print(team_list)
    return filter_teams(team_list)


def filter_teams(teams: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """
    Filters the list of teams to remove duplicates or irrelevant entries.
    """
    return [
        team for team in teams
        if "academy" not in team[1].lower() and "challenger" not in team[1].lower()
    ]
