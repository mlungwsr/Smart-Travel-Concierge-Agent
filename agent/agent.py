"""
Smart Travel Concierge Agent
Built with Strands Agents + Amazon Bedrock AgentCore
"""

import json
from datetime import datetime, timezone
import boto3
from strands import Agent, tool
from bedrock_agentcore.runtime import BedrockAgentCoreApp

REGION = "us-west-2"
lambda_client = boto3.client("lambda", region_name=REGION)

app = BedrockAgentCoreApp()
log = app.logger


def build_system_prompt():
    now = datetime.now(timezone.utc)
    return f"""You are a Smart Travel Concierge — a friendly, knowledgeable travel assistant.

IMPORTANT — Current date/time: {now.strftime('%A, %B %d, %Y at %H:%M UTC')}
Always use this as your reference for "today", "this weekend", "next week", etc.

Your capabilities:
- Search for flights between cities worldwide
- Check current weather and forecasts for any destination
- Remember user preferences across conversations

Guidelines:
- Always be warm, helpful, and enthusiastic about travel
- When presenting flight options, format them clearly with airlines, times, and status
- When discussing weather, relate it to packing and activity recommendations
- If the user has stated preferences (dietary, seating, home airport), always factor them in
- Use USD for prices unless the user specifies otherwise
- For African destinations, highlight local culture and must-see attractions
- The flight search tool returns real-time data for today's flights only. For future dates, it returns simulated data to illustrate typical routes and pricing.
"""


@tool
def search_flights(origin: str, destination: str, date: str = "", num_results: int = 5) -> str:
    """Search for flights between two cities.

    Args:
        origin: Departure city name (e.g., 'Johannesburg', 'Lagos', 'London')
        destination: Arrival city name (e.g., 'Cape Town', 'Nairobi', 'Dubai')
        date: Travel date in YYYY-MM-DD format (optional, defaults to today)
        num_results: Number of flight results to return (default 5)
    """
    response = lambda_client.invoke(
        FunctionName="travel-flight-search",
        Payload=json.dumps({
            "origin": origin,
            "destination": destination,
            "date": date,
            "num_results": num_results,
        }),
    )
    result = json.loads(response["Payload"].read())
    return result.get("body", json.dumps(result))


@tool
def check_weather(city: str) -> str:
    """Check current weather and 5-day forecast for a city.

    Args:
        city: City name to check weather for (e.g., 'Cape Town', 'Nairobi')
    """
    response = lambda_client.invoke(
        FunctionName="travel-weather-lookup",
        Payload=json.dumps({"city": city}),
    )
    result = json.loads(response["Payload"].read())
    return result.get("body", json.dumps(result))


@tool
def get_current_datetime() -> str:
    """Get the current date and time in UTC. Use this when you need to know today's date."""
    now = datetime.now(timezone.utc)
    return json.dumps({
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S UTC"),
        "day_of_week": now.strftime("%A"),
        "iso": now.isoformat(),
    })


_agent = None

def get_or_create_agent():
    global _agent
    _agent = Agent(
        model="us.amazon.nova-pro-v1:0",
        system_prompt=build_system_prompt(),
        tools=[search_flights, check_weather, get_current_datetime],
    )
    return _agent


@app.entrypoint
async def invoke(payload, context):
    log.info("Invoking Travel Concierge Agent...")
    agent = get_or_create_agent()
    stream = agent.stream_async(payload.get("prompt"))
    async for event in stream:
        if "data" in event and isinstance(event["data"], str):
            yield event["data"]


if __name__ == "__main__":
    app.run()
