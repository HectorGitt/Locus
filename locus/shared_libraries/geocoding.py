import os
import requests


def geocode_location(location: str) -> dict:
    """
    Geocodes a location string to latitude and longitude coordinates.

    Args:
        location (str): The location string to geocode (e.g., "New York, NY" or "Paris, France").

    Returns:
        dict: A dictionary containing:
            - "lat": latitude coordinate
            - "lng": longitude coordinate
            - "formatted_address": the formatted address from Google
            - "error": error message if geocoding fails

    Example:
        >>> result = geocode_location("Mountain View, CA")
        >>> print(result)
        {"lat": 37.3900264, "lng": -122.0812304, "formatted_address": "Mountain View, CA, USA"}
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY not found in .env file."}

    try:
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        geocode_params = {"address": location, "key": api_key}

        geocode_response = requests.get(geocode_url, params=geocode_params)
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()

        if not geocode_data.get("results"):
            return {"error": f"Could not find location: {location}"}

        # Get the first result
        result = geocode_data["results"][0]
        location_data = result["geometry"]["location"]

        return {
            "lat": location_data["lat"],
            "lng": location_data["lng"],
            "formatted_address": result.get("formatted_address", location),
        }

    except Exception as e:
        return {"error": f"Failed to geocode location '{location}': {str(e)}"}
