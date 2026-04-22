"""
Smart Travel Concierge — Weather Lookup Lambda
Calls wttr.in free API for real weather data, with mock fallback.
"""

import json
import random
from urllib import request, error


def fetch_weather(city: str) -> dict:
    """Try wttr.in first, fall back to mock data."""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        req = request.Request(url, headers={"User-Agent": "SmartTravelConcierge/1.0"})
        with request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())

        current = data["current_condition"][0]
        forecast_days = []
        for day in data.get("weather", [])[:5]:
            forecast_days.append({
                "date": day["date"],
                "max_temp_c": day["maxtempC"],
                "min_temp_c": day["mintempC"],
                "description": day["hourly"][4]["weatherDesc"][0]["value"],
                "chance_of_rain": day["hourly"][4]["chanceofrain"],
            })

        return {
            "source": "wttr.in",
            "city": city,
            "current": {
                "temp_c": current["temp_C"],
                "feels_like_c": current["FeelsLikeC"],
                "humidity": current["humidity"],
                "description": current["weatherDesc"][0]["value"],
                "wind_speed_kmh": current["windspeedKmph"],
            },
            "forecast": forecast_days,
        }
    except Exception:
        return generate_mock_weather(city)


def generate_mock_weather(city: str) -> dict:
    random.seed(hash(city) % 2**32)
    conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Clear"]
    return {
        "source": "mock",
        "city": city,
        "current": {
            "temp_c": str(random.randint(15, 35)),
            "feels_like_c": str(random.randint(14, 36)),
            "humidity": str(random.randint(30, 80)),
            "description": random.choice(conditions),
            "wind_speed_kmh": str(random.randint(5, 30)),
        },
        "forecast": [
            {
                "date": f"Day {i+1}",
                "max_temp_c": str(random.randint(20, 35)),
                "min_temp_c": str(random.randint(10, 20)),
                "description": random.choice(conditions),
                "chance_of_rain": str(random.randint(0, 60)),
            }
            for i in range(5)
        ],
    }


def lambda_handler(event, context):
    body = event.get("body")
    if isinstance(body, str):
        body = json.loads(body)
    elif body is None:
        body = event

    city = body.get("city", "Cape Town")
    weather = fetch_weather(city)

    return {
        "statusCode": 200,
        "body": json.dumps(weather),
    }
