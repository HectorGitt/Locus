import os
import googlemaps
from typing import Optional
from locus.shared_libraries.geocoding import geocode_location


def suggest_experiences(
    location: str, mood: Optional[str] = None, weather: Optional[str] = None
) -> dict:
    """
    Suggests experiences based on location, mood, or weather using Google Places API.

    Args:
        location (str): The location to find experiences.
        mood (str, optional): The user's current mood (e.g., "adventurous", "relaxed").
        weather (str, optional): The current weather (e.g., "sunny", "rainy").

    Returns:
        dict: A dictionary containing a list of suggested experiences.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY not found in .env file."}

    gmaps = googlemaps.Client(key=api_key)

    try:
        # Geocode the location using shared utility
        geocode_result = geocode_location(location)
        if "error" in geocode_result:
            return {"error": geocode_result["error"]}

        lat = geocode_result["lat"]
        lng = geocode_result["lng"]

        # Determine place types based on mood and weather
        place_types = []
        if mood == "adventurous":
            place_types = ["amusement_park", "park", "campground"]
        elif mood == "relaxed":
            place_types = ["park", "cafe", "spa"]
        elif weather == "sunny":
            place_types = ["beach", "park", "outdoor_activity"]
        elif weather == "rainy":
            place_types = ["museum", "movie_theater", "shopping_mall"]
        else:
            place_types = ["tourist_attraction", "point_of_interest"]

        experiences = []
        for place_type in place_types[
            :2
        ]:  # Limit to 2 types to avoid too many API calls
            places_result = gmaps.places_nearby(
                location=(lat, lng),
                radius=10000,  # 10km radius
                type=place_type,
            )
            for place in places_result.get("results", [])[:3]:  # 3 per type
                name = place.get("name", "Unknown")
                rating = place.get("rating", "N/A")
                experiences.append(f"{name} (Rating: {rating})")

        if not experiences:
            return {
                "message": f"No specific experiences found for {location} with the given criteria."
            }

        return {"experiences": experiences[:5]}  # Limit to 5 suggestions

    except Exception as e:
        return {"error": str(e)}
