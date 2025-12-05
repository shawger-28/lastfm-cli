import argparse


def build_parser():
    parser = argparse.ArgumentParser(
        prog="lastfm",
        description="Show last.fm listening history",
    )

    parser.add_argument(
        "-l", "--limit",
        type=int,
        help="Number of tracks to display",
    )

    parser.add_argument(
        "-u", "--user",
        help="Override username",
    )

    parser.add_argument(
    	"--live",
    	action="store_true",
    	help="Continuously update the track list",
    )
    return parser
