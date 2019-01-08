import requests

from aspettami.config import API_URL


def search_stop(query: str):
    data = {"url": f"tpPortal/tpl/stops/search/{query}"}
    res = requests.post(API_URL, data=data)
    return res.json()


def get_stop_info(stop_code: str):
    data = {"url": f"tpPortal/geodata/pois/{stop_code}?lang=it"}
    res = requests.post(API_URL, data=data)
    return res.json()
