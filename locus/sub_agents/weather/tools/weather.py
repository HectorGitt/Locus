import os
import requests
from typing import Optional


def get_weather(location: str, days_ahead: Optional[int] = 0) -> dict:
    """
    Gets weather information for a location using Google Custom Search.

    Args:
        location (str): The city or location to get weather for.
        days_ahead (int, optional): Number of days ahead from today (0 = today, 1 = tomorrow, etc.). Defaults to 0.

    Returns:
        dict: A dictionary containing weather information.
    """
    api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_CSE_ID")

    if not api_key or not search_engine_id:
        return {
            "error": "GOOGLE_CUSTOM_SEARCH_API_KEY or GOOGLE_CUSTOM_SEARCH_CSE_ID not found in .env file."
        }

    # Build query based on days ahead
    if days_ahead == 0:
        query = f"current weather in {location}"
    elif days_ahead == 1:
        query = f"weather tomorrow in {location}"
    else:
        query = f"weather {days_ahead} days from now in {location}"

    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": query,
            "num": 5,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("items", []):
            result = {
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
            }
            results.append(result)

        if not results:
            return {"error": f"No weather information found for {location}."}

        return {
            "location": location,
            "forecast_type": "current" if days_ahead == 0 else f"{days_ahead} days ahead",
            "weather_info": results[:3]  # Return top 3 results
        }

    except Exception:
        return {"error": f"Failed to fetch weather information for {location}."}