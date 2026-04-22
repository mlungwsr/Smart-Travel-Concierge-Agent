"""
Smart Travel Concierge — Flight Search Lambda
Returns mock flight data for demo purposes.
"""

import json
import random
from datetime import datetime, timedelta

AIRLINES = [
    {"code": "SA", "name": "South African Airways"},
    {"code": "KQ", "name": "Kenya Airways"},
    {"code": "ET", "name": "Ethiopian Airlines"},
    {"code": "EK", "name": "Emirates"},
    {"code": "BA", "name": "British Airways"},
    {"code": "QR", "name": "Qatar Airways"},
    {"code": "TK", "name": "Turkish Airlines"},
]

AIRPORTS = {
    "johannesburg": "JNB", "cape town": "CPT", "durban": "DUR",
    "nairobi": "NBO", "lagos": "LOS", "accra": "ACC",
    "cairo": "CAI", "addis ababa": "ADD", "dar es salaam": "DAR",
    "london": "LHR", "dubai": "DXB", "new york": "JFK",
    "paris": "CDG", "tokyo": "NRT", "sydney": "SYD",
    "mumbai": "BOM", "singapore": "SIN", "bangkok": "BKK",
}


def resolve_airport(city: str) -> str:
    city_lower = city.strip().lower()
    return AIRPORTS.get(city_lower, city.upper()[:3])


def generate_flights(origin: str, destination: str, date: str, num_results: int = 5):
    random.seed(hash(f"{origin}{destination}{date}") % 2**32)
    base_price = random.randint(200, 1200)
    flights = []
    for i in range(num_results):
        airline = random.choice(AIRLINES)
        dep_hour = random.randint(5, 22)
        dep_min = random.choice([0, 15, 30, 45])
        duration_hrs = random.randint(1, 14)
        duration_min = random.choice([0, 15, 30, 45])
        price = base_price + random.randint(-150, 300)
        price = max(price, 99)
        stops = random.choices([0, 1, 2], weights=[50, 35, 15])[0]
        flights.append({
            "flight_number": f"{airline['code']}{random.randint(100,999)}",
            "airline": airline["name"],
            "origin": origin,
            "destination": destination,
            "departure_date": date,
            "departure_time": f"{dep_hour:02d}:{dep_min:02d}",
            "duration": f"{duration_hrs}h {duration_min}m",
            "stops": stops,
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
    date = body.get("date", (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))
    num_results = int(body.get("num_results", 5))

    origin_code = resolve_airport(origin)
    dest_code = resolve_airport(destination)
    flights = generate_flights(origin_code, dest_code, date, num_results)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "search_query": {
                "origin": f"{origin} ({origin_code})",
                "destination": f"{destination} ({dest_code})",
                "date": date,
            },
            "results_count": len(flights),
            "flights": flights,
        }),
    }
