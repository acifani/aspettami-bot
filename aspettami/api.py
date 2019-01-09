import json
from typing import List

import requests

from aspettami.config import API_URL
from aspettami.stop import Stop
from aspettami.logger import logger


def search_stop(query: str) -> List[Stop]:
    data = {"url": f"tpPortal/tpl/stops/search/{query}"}
    stops = [Stop(stop) for stop in _call(data)]
    return [stop for stop in stops if stop.is_bus_or_tram_stop()]


def get_stop_info(stop_code: str) -> Stop:
    data = {"url": f"tpPortal/geodata/pois/{stop_code}?lang=it"}
    return Stop(_call(data))


def _call(data):
    try:
        logger.debug("Calling API")
        logger.debug(data)
        res = requests.post(API_URL, data=data)
        return res.json()
    except json.decoder.JSONDecodeError:
        logger.debug("Empty response")
        return None
