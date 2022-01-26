import json
from typing import List

import requests

from aspettami.config import API_URL
from aspettami.stop import Stop
from aspettami.logger import logger

# workaround for server not supporting diffie-hellman
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "HIGH:!DH:!aNULL"


def search_stop(query: str) -> List[Stop]:
    data = {"url": f"tpPortal/tpl/stops/search/{query}"}
    stops = [Stop(stop) for stop in _call(data) or list()]
    return [stop for stop in stops if stop.is_bus_or_tram_stop()]


def get_stop_info(stop_code: str) -> Stop:
    data = {"url": f"tpPortal/geodata/pois/{stop_code}?lang=it"}
    return Stop(_call(data))


def _call(data):
    try:
        logger.debug("Calling API")
        logger.debug(data)
        headers = {
            "Origin": "https://giromilano.atm.it",
            "Referer": "https://giromilano.atm.it/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        }
        res = requests.post(API_URL, data=data, headers=headers)
        return res.json()
    except json.decoder.JSONDecodeError:
        logger.debug("Empty response")
        return None
