import os
from functools import partial
from logging import Logger
from typing import Callable

import requests

from icewatch.geocode.mapbox import query_mapbox
from icewatch.geocode.types import Coordinates

geocode_address: Callable[[str, Logger, requests.Session | None], Coordinates | None]

MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN")
if MAPBOX_ACCESS_TOKEN:
    geocode_address = partial(query_mapbox, MAPBOX_ACCESS_TOKEN)
else:
    from icewatch.geocode.nomination import geocode_address


__all__ = ["geocode_address"]
