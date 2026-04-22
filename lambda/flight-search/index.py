"""
Smart Travel Concierge — Flight Search Lambda
Calls AviationStack API for real flight data, falls back to mock.
API key stored in SSM Parameter Store.
"""

import json
import os
import random
from datetime import datetime, timedelta
from urllib import request, error, parse

import boto3

REGION = os.environ.get("AWS_REGION", "us-west-2")
SSM_KEY = "/travel-concierge/aviationstack-api-key"
_api_key = None

AIRPORTS = {
    "johannesburg": "JNB", "cape town": "CPT", "durban": "DUR",
    "nairobi": "NBO", "lagos": "LOS", "accra": "ACC",
    "cairo": "CAI", "addis ababa": "ADD", "dar es salaam": "DAR",
    "london": "LHR", "dubai": "DXB", "new york": "JFK",
    "paris": "CDG", "tokyo": "NRT", "sydney": "SYD",
    "mumbai": "BOM", "singapore": "SIN", "bangkok": "BKK",
}

AIRLINES = [
    {"code": "SA", "name": "South African Airways"},
    {"code": "KQ", "name": "Kenya Airways"},
    {"code": "ET", "name": "Ethiopian Airlines"},
    {"code": "EK", "name": "Emirates"},
    {"code": "BA", "name": "British Airways"},
    {"code": "QR", "name": "Qatar Airways"},
    {"code": "TK", "name": "Turkish Airlines"},
]


def get_api_key():
    global _api_key
    if _api_key is None:
        ssm = boto3.client("ssm", region_name=REGION)
        _api_key = ssm.get_parameter(Name=SSM_KEY, WithDecryption=True)["Parameter"]["Value"]
    return _api_key


def resolve_airport(city: str) -> str:
    return AIRPORTS.get(city.strip().lower(), city.upper()[:3])


def fetch_real_flights(dep_iata: str, arr_iata: str, limit: int = 5):
    """Call AviationStack /v1/flights endpoint."""
    key = get_api_key()
    params = parse.urlencode({
        "access_key": key,
        "dep_iata": dep_iata,
        "arr_iata": arr_iata,
        "limit": limit,
    })
    url = f"http://api.aviationstack.com/v1/flights?{params}"
    req = request.Request(url, headers={"User-Agent": "SmartTravelConcierge/1.0"})
    with request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read().decode())

    if "data" not in data or not data["data"]:
        raise ValueError("No flight data returned")

    flights = []
    for f in data["data"][:limit]:
        dep = f.get("departure", {})
        arr = f.get("arrival", {})
        airline = f.get("airline", {})
        flight_info = f.get("flight", {})
        flights.append({
            "flight_number": flight_info.get("iata", "N/A"),
            "airline": airline.get("name", "Unknown"),
            "origin": dep.get("iata", dep_iata),
            "destination": arr.get("iata", arr_iata),
            "departure_date": f.get("flight_date", "N/A"),
            "departure_time": (dep.get("scheduled") or "N/A")[:16],
            "arrival_time": (arr.get("scheduled") or "N/A")[:16],
            "flight_status": f.get("flight_status", "unknown"),
            "departure_airport": dep.get("airport", "N/A"),
            "arrival_airport": arr.get("airport", "N/A"),
            "departure_terminal": dep.get("terminal"),
            "departure_gate": dep.get("gate"),
        })
    return flights


def generate_mock_flights(origin, destination, date, num_results=5):
    random.seed(hash(f"{origin}{destination}{date}") % 2**32)
    base_price = random.randint(200, 1200)
    flights = []
    for _ in range(num_results):
        a = random.choice(AIRLINES)
        price = max(base_price + random.randint(-150, 300), 99)
        flights.append({
            "flight_number": f"{a['code']}{random.randint(100,999)}",
            "airline": a["name"],
            "origin": origin, "destination": destination,
            "departure_date": date,
            "departure_time": f"{random.randint(5,22):02d}:{random.choice([0,15,30,45]):02d}",
            "duration": f"{random.randint(1,14)}h {random.choice([0,15,30,45])}m",
            "stops": random.choices([0, 1, 2], weights=[50, 35, 15])[0],
            "price_usd": price,
            "cabin_class": "Economy",
            "seats_available": random.randint(1, 42),
        })
    flights.sort(key=lambda f: f["price_usd"])
    return flights


def lambda_handler(event, context):
    body = event.get("body")
    if isinstance(body, str):
        body = json.loads(body)
    elif body is None:
        body = event

    origin = body.get("origin", "Johannesburg")
    destination = body.get("destination", "Cape Town")
    date = body.get("date", "")
    num_results = int(body.get("num_results", 5))

    origin_code = resolve_airport(origin)
    dest_code = resolve_airport(destination)

    try:
        today = datetime.now().strftime("%Y-%m-%d")
        is_today = (not date) or (date == today)
        if is_today:
            flights = fetch_real_flights(origin_code, dest_code, num_results)
            source = "aviationstack"
        else:
            flights = generate_mock_flights(origin_code, dest_code, date, num_results)
            source = "mock (future date)"
    except Exception as e:
        print(f"AviationStack API failed ({e}), using mock data")
        flights = generate_mock_flights(origin_code, dest_code, date, num_results)
        source = "mock"

    return {
        "statusCode": 200,
        "body": json.dumps({
            "source": source,
            "search_query": {
                "origin": f"{origin} ({origin_code})",
                "destination": f"{destination} ({dest_code})",
                "date": date,
            },
            "results_count": len(flights),
            "flights": flights,
        }),
    }
