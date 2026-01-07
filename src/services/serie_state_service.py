from fetch.serie_state import fetch_serie_state
from caching.series_state import get_cached_series, cache_series_state

def get_serie_state(series_id: str) -> dict:
    cached = get_cached_series(series_id)
    if cached:
        return cached
    data = fetch_serie_state(series_id)

    cache_series_state(series_id, data)
    return data

def get_series_states(series_ids: list[str]) -> list[dict]:
    series_states = []

    for sid in series_ids:
        try: 
            state = get_serie_state(sid)
            series_states.append(state)
        except Exception as e:
            print(f" ⚠️ Failed to retrieve state for ID: {sid}. Error: {e}")
    return series_states

if __name__ == "__main__":
    test_id = "2843060"
    print(f"Testing get_serie_state for ID: {test_id}")
    state = get_serie_state(test_id)
    print(f"Keys in state: {list(state)}")

