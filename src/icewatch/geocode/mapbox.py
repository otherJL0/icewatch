from icewatch.geocode.types import Coordinates
from logging import Logger

import requests


MAPBOX_URL = "https://api.mapbox.com/search/geocode/v6/forward"


def query_mapbox(
    access_token: str,
    address: str,
    logger: Logger,
    session: requests.Session | None = None,
) -> Coordinates | None:
    logger.info("MAPBOX_ACCESS_TOKEN found, using Mapbox api")
    params: dict[str, str | int] = {
        "q": address,
        "access_token": access_token,
        "limit": 1,
    }

    s = session or requests.Session()
    response = s.get(MAPBOX_URL, params=params)
    response.raise_for_status()
    if result := response.json():
        feature = result["features"][0]
        coordinates = feature["properties"]["coordinates"]
        return {
            "lat": float(coordinates["latitude"]),
            "lon": float(coordinates["longitude"]),
        }
    return None
