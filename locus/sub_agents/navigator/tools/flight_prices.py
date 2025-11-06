import os
import requests
from datetime import datetime, timedelta
from typing import Optional


def find_flight_prices(
    origin: str, destination: str, date: Optional[str] = None
) -> dict:
    """
    Finds flight prices using Google Custom Search on price comparison sites.

    Args:
        origin (str): The origin city or airport.
        destination (str): The destination city or airport.
        date (str, optional): The travel date. Can be a specific date (YYYY-MM-DD),
                              or relative like "tomorrow", "next Saturday", etc.

    Returns:
        dict: A dictionary containing flight price search results.
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

    # Search on price comparison sites
    query = f"cheap flights from {origin} to {destination}"
    if date:
        query += f" {date}"

    # Add site-specific searches for price comparison
    site_queries = [
        f"{query} site:kayak.com",
        f"{query} site:skyscanner.com",
        f"{query} site:google.com/flights",
        f"{query} site:momondo.com",
    ]

    all_results = []
    for site_query in site_queries:
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": api_key,
                "cx": search_engine_id,
                "q": site_query,
                "num": 3,
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            for item in data.get("items", []):
                result = {
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet"),
                    "source": site_query.split("site:")[1].split()[0]
                    if "site:" in site_query
                    else "general",
                }
                all_results.append(result)

        except Exception:
            continue  # Skip failed site searches

    if not all_results:
        return {"error": "No flight price results found."}

    return {"flight_prices": all_results[:10]}  # Limit to 10 results


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
