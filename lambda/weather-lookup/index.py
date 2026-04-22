"""
Smart Travel Concierge — Weather Lookup Lambda
Calls WeatherAPI.com for real weather data, falls back to mock.
API key stored in SSM Parameter Store.
"""

import json
import os
import random
from urllib import request, parse

import boto3

REGION = os.environ.get("AWS_REGION", "us-west-2")
SSM_KEY = "/travel-concierge/weatherapi-api-key"
_api_key = None


def get_api_key():
    global _api_key
    if _api_key is None:
        ssm = boto3.client("ssm", region_name=REGION)
        _api_key = ssm.get_parameter(Name=SSM_KEY, WithDecryption=True)["Parameter"]["Value"]
    return _api_key


def fetch_real_weather(city: str) -> dict:
    """Call WeatherAPI.com forecast endpoint."""
    key = get_api_key()
    params = parse.urlencode({"key": key, "q": city, "days": 5, "aqi": "no"})
    url = f"http://api.weatherapi.com/v1/forecast.json?{params}"
    req = request.Request(url, headers={"User-Agent": "SmartTravelConcierge/1.0"})
    with request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read().decode())

    current = data["current"]
    forecast_days = []
    for day in data.get("forecast", {}).get("forecastday", []):
        d = day["day"]
        forecast_days.append({
            "date": day["date"],
            "max_temp_c": str(d["maxtemp_c"]),
            "min_temp_c": str(d["mintemp_c"]),
            "description": d["condition"]["text"],
            "chance_of_rain": str(d["daily_chance_of_rain"]),
            "avg_humidity": str(d["avghumidity"]),
        })

    return {
        "source": "weatherapi.com",
        "city": data["location"]["name"],
        "country": data["location"]["country"],
        "current": {
            "temp_c": str(current["temp_c"]),
            "feels_like_c": str(current["feelslike_c"]),
            "humidity": str(current["humidity"]),
            "description": current["condition"]["text"],
            "wind_speed_kmh": str(current["wind_kph"]),
            "uv_index": str(current["uv"]),
        },
        "forecast": forecast_days,
    }


def generate_mock_weather(city: str) -> dict:
    random.seed(hash(city) % 2**32)
    conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Clear"]
    return {
        "source": "mock",
        "city": city,
        "country": "Unknown",
        "current": {
            "temp_c": str(random.randint(15, 35)),
            "feels_like_c": str(random.randint(14, 36)),
            "humidity": str(random.randint(30, 80)),
            "description": random.choice(conditions),
            "wind_speed_kmh": str(random.randint(5, 30)),
            "uv_index": str(random.randint(1, 10)),
        },
        "forecast": [
            {
                "date": f"Day {i+1}",
                "max_temp_c": str(random.randint(20, 35)),
                "min_temp_c": str(random.randint(10, 20)),
                "description": random.choice(conditions),
                "chance_of_rain": str(random.randint(0, 60)),
                "avg_humidity": str(random.randint(30, 80)),
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

    try:
        weather = fetch_real_weather(city)
    except Exception as e:
        print(f"WeatherAPI.com failed ({e}), using mock data")
        weather = generate_mock_weather(city)

    return {
        "statusCode": 200,
        "body": json.dumps(weather),
    }
