import sys

from lastfm.config import load_config, ConfigError
from lastfm.api import get_recent_tracks, APIError, NetworkError, InvalidResponseError
from lastfm.format import format_tracks
from lastfm.parser import build_parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        config = load_config()
    except ConfigError as e:
        print(f"Config error: {e}")
        sys.exit(1)

    username = args.user if args.user else config["username"]
    limit = args.limit if args.limit else config["default_limit"]

    try:
        tracks = get_recent_tracks(
            username=username,
            api_key=config["api_key"],
            limit=limit,
        )
    except (APIError, NetworkError, InvalidResponseError) as e:
        print(f"API error: {e}")
        sys.exit(1)

    formatted = format_tracks(tracks)

    for item in formatted:
        print(item)
        print("-" * 40)


if __name__ == "__main__":
    main()
