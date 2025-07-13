import argparse
import sys

import icewatch.geocode_facilities as geocoder
import icewatch.ice_detention_scraper as scraper
import icewatch.render_facilities_map as renderer


def main():
    parser = argparse.ArgumentParser(prog="icewatch")

    subparsers = parser.add_subparsers(
        dest="command",
        help="available commands",
        required=True,
    )
    subparsers.add_parser("scrape", add_help=False)
    subparsers.add_parser("geocode", add_help=False)
    subparsers.add_parser("render", add_help=False)

    args, remaining_argv = parser.parse_known_args()
    sys.argv = [f"{sys.argv[0]}"] + remaining_argv
    match args.command:
        case "scrape":
            return scraper.main()
        case "geocode":
            return geocoder.main()
        case "render":
            return renderer.main()
        case _:
            sys.exit(1)
