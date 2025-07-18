# level_api.py
import requests 
from operator import itemgetter
import json
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
        "Referer": "https://www.flylevel.com/",
        "Origin": "https://www.flylevel.com"
    }
    r = requests.get(BASE, params=params, headers=headers, timeout=20)
    try:
        r.raise_for_status()
        data = r.json()
        print(json.dumps(data, indent=2))
        return data.get("data", {}).get("dayPrices", [])
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return []

def cheapest_day(origin, dest, outbound, year, month):
    return min(
        get_month_prices(origin, dest, outbound, year, month),
        key=itemgetter("price")
    )
