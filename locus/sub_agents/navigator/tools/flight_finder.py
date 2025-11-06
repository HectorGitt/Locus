import os
import requests
from datetime import datetime, timedelta
from typing import Optional


def find_flights(origin: str, destination: str, date: Optional[str] = None) -> dict:
    """
    Finds flights between two locations using Google Custom Search API.

    Args:
        origin (str): The origin city or airport.
        destination (str): The destination city or airport.
        date (str, optional): The travel date. Can be a specific date (YYYY-MM-DD),
                              or relative like "tomorrow", "next Saturday", etc.

    Returns:
        dict: A dictionary containing flight search results.
    """
    api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_CSE_ID")

    if not api_key or not search_engine_id:
        return {
            "error": "GOOGLE_CUSTOM_SEARCH_API_KEY or GOOGLE_CUSTOM_SEARCH_CSE_ID not found in .env file."
        }

    # Parse relative dates
    if date:
        date = parse_relative_date(date)

    query = f"flights from {origin} to {destination}"
    if date:
        query += f" on {date}"

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        "num": 5,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("items", []):
            results.append(
                {
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet"),
                }
            )

        return {"flights": results}

    except Exception as e:
        return {"error": str(e)}


def parse_relative_date(date_str: str) -> str:
    """
    Parses relative date strings into YYYY-MM-DD format.

    Args:
        date_str (str): Relative date like "tomorrow", "next Saturday", etc.

    Returns:
        str: Date in YYYY-MM-DD format.
    """
    today = datetime.now()
    date_str = date_str.lower().strip()

    if date_str == "today":
        return today.strftime("%Y-%m-%d")
    elif date_str == "tomorrow":
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif "saturday" in date_str:
        # Find next Saturday (weekday 5)
        days_ahead = (5 - today.weekday()) % 7
        if days_ahead == 0:  # Today is Saturday
            days_ahead = 7
        target_date = today + timedelta(days=days_ahead)
        return target_date.strftime("%Y-%m-%d")
    elif "sunday" in date_str:
        days_ahead = (6 - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        target_date = today + timedelta(days=days_ahead)
        return target_date.strftime("%Y-%m-%d")
    else:
        # Try to parse as YYYY-MM-DD
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            # Return as-is if can't parse
            return date_str
