import argparse
import sys

import icewatch.geocode_facilities as geocoder
import icewatch.ice_detention_scraper as scraper
import icewatch.render_facilities_map as renderer


def main():
    parser = argparse.ArgumentParser(
        prog="icewatch",
        description="Command line tool to download ICE detention statistics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Example Usage:
    icewatch scrape
    icewatch geocode --input data/ice_facilities_20250704_162107.json
    icewatch render  --input data/facilities_geocoded_20250704_162107.json""",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        required=True,
    )
    subparsers.add_parser(
        name="scrape",
        add_help=False,
        help="Download ICE detention statistics Excel file",
    )
    subparsers.add_parser(
        name="geocode",
        add_help=False,
        help="Geocode facilities JSON using OpenStreetMap Nominatim with caching.",
    )
    subparsers.add_parser(
        name="render", add_help=False, help="Render a static HTML map of facilities."
    )

    args, argv_tail = parser.parse_known_args()
    sys.argv = [
        f"{sys.argv[0]} {args.command}"
    ] + argv_tail  # modify sys.argv to remove subcommand
    match args.command:
        case "scrape":
            return scraper.main()
        case "geocode":
            return geocoder.main()
        case "render":
            return renderer.main()
        case _:
            sys.exit(1)
