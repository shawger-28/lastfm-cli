import requests


class APIError(Exception):
    """Raised when the API returns an error."""
    pass


class NetworkError(Exception):
    """Raised when a network error occurs."""
    pass


class InvalidResponseError(Exception):
    """Raised when the API response is malformed."""
    pass


BASE_URL = "https://ws.audioscrobbler.com/2.0/"


def get_recent_tracks(username, api_key, limit):
    params = {
        "method": "user.getrecenttracks",
        "user": username,
        "api_key": api_key,
        "limit": limit,
        "format": "json",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.RequestException as e:
        raise NetworkError(f"Network error while contacting Last.fm: {e}")

    if response.status_code != 200:
        raise APIError(
            f"API returned HTTP {response.status_code}: {response.text}"
        )

    try:
        data = response.json()
    except ValueError:
        raise InvalidResponseError("API did not return valid JSON")

    if "error" in data:
        message = data.get("message", "Unknown API error")
        raise APIError(f"Last.fm API error: {message}")

    try:
        tracks = data["recenttracks"]["track"]
    except (KeyError, TypeError):
        raise InvalidResponseError("Unexpected API response format")

    return tracks
