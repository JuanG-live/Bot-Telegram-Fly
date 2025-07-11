# level_api.py
import requests 
from operator import itemgetter

BASE = "https://www.flylevel.com/nwe/flights/api/calendar/"

def get_month_prices(origin, dest, outbound, year, month, cur="EUR"):
    params = {
        "triptype": "RT",
        "origin": origin,
        "destination": dest,
        "outboundDate": outbound,
        "year": year,
        "month": month,
        "currencyCode": cur
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.flylevel.com/"
    }
    r = requests.get(BASE, params=params, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()["data"]["dayPrices"]

def cheapest_day(origin, dest, outbound, year, month):
    return min(
        get_month_prices(origin, dest, outbound, year, month),
        key=itemgetter("price")
    )
