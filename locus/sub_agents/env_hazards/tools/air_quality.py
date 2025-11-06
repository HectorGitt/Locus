import os
import requests


def check_air_quality(location: str) -> dict:
    """
    Checks air quality index and pollution levels for a location.

    Args:
        location (str): The city or location to check air quality for.

    Returns:
        dict: A dictionary containing air quality information.
    """
    api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_CSE_ID")

    if not api_key or not search_engine_id:
        return {
            "error": "GOOGLE_CUSTOM_SEARCH_API_KEY or GOOGLE_CUSTOM_SEARCH_CSE_ID not found in .env file."
        }

    try:
        # Search for air quality information
        query = f"air quality index {location} current"
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
            return {"error": f"No air quality information found for {location}."}

        return {
            "location": location,
            "air_quality_info": results[:3],  # Return top 3 results
        }

    except Exception:
        return {"error": f"Failed to fetch air quality information for {location}."}


def check_environmental_hazards(location: str) -> dict:
    """
    Checks for environmental hazards like natural disasters, pollution alerts, etc.

    Args:
        location (str): The location to check for environmental hazards.

    Returns:
        dict: A dictionary containing environmental hazard information.
    """
    api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_CSE_ID")

    if not api_key or not search_engine_id:
        return {
            "error": "GOOGLE_CUSTOM_SEARCH_API_KEY or GOOGLE_CUSTOM_SEARCH_CSE_ID not found in .env file."
        }

    try:
        # Search for environmental hazards and warnings
        query = f"environmental hazards warnings alerts {location}"
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
            return {
                "message": f"No current environmental hazards found for {location}."
            }

        return {
            "location": location,
            "environmental_hazards": results[:3],  # Return top 3 results
        }

    except Exception:
        return {
            "error": f"Failed to fetch environmental hazard information for {location}."
        }


def check_travel_warnings(location: str) -> dict:
    """
    Checks for travel warnings, advisories, and safety alerts for a location.

    Args:
        location (str): The location to check for travel warnings.

    Returns:
        dict: A dictionary containing travel warning information.
    """
    api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_CSE_ID")

    if not api_key or not search_engine_id:
        return {
            "error": "GOOGLE_CUSTOM_SEARCH_API_KEY or GOOGLE_CUSTOM_SEARCH_CSE_ID not found in .env file."
        }

    try:
        # Search for travel warnings and advisories
        query = f"travel warnings advisories {location} state department"
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
            return {"message": f"No current travel warnings found for {location}."}

        return {
            "location": location,
            "travel_warnings": results[:3],  # Return top 3 results
        }

    except Exception:
        return {"error": f"Failed to fetch travel warning information for {location}."}
