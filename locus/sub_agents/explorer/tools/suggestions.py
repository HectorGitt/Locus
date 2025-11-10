import os
import googlemaps
from typing import Optional
from locus.shared_libraries.geocoding import geocode_location


def suggest_experiences(
    location: str, 
    preferences: Optional[str] = None, 
    weather: Optional[str] = None
) -> dict:
    """
    Suggests experiences based on location, user preferences, or weather using Google Places API.

    Args:
        location (str): The location to find experiences.
        preferences (str, optional): What the user is looking for (e.g., "adventure activities", "cultural sites", "relaxation", "nightlife", "family-friendly").
        weather (str, optional): The current weather conditions (e.g., "sunny", "rainy").

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

        # Determine place types based on preferences and weather
        place_types = []
        if preferences:
            pref_lower = preferences.lower()
            if "adventure" in pref_lower or "active" in pref_lower or "outdoor" in pref_lower:
                place_types = ["amusement_park", "park", "campground", "hiking_area"]
            elif "relax" in pref_lower or "calm" in pref_lower or "peaceful" in pref_lower:
                place_types = ["park", "cafe", "spa", "library"]
            elif "culture" in pref_lower or "art" in pref_lower or "history" in pref_lower:
                place_types = ["museum", "art_gallery", "historical_site", "church"]
            elif "food" in pref_lower or "dining" in pref_lower or "restaurant" in pref_lower:
                place_types = ["restaurant", "cafe", "bar", "food"]
            elif "shop" in pref_lower or "shopping" in pref_lower:
                place_types = ["shopping_mall", "store", "market"]
            elif "nightlife" in pref_lower or "night" in pref_lower or "party" in pref_lower:
                place_types = ["night_club", "bar", "casino"]
            elif "family" in pref_lower or "kids" in pref_lower:
                place_types = ["amusement_park", "zoo", "aquarium", "park"]
            else:
                place_types = ["tourist_attraction", "point_of_interest"]
        elif weather:
            if weather.lower() in ["sunny", "clear", "nice"]:
                place_types = ["park", "beach", "outdoor_activity", "hiking_area"]
            elif weather.lower() in ["rainy", "wet", "cold"]:
                place_types = ["museum", "movie_theater", "shopping_mall", "cafe"]
            else:
                place_types = ["tourist_attraction", "point_of_interest"]
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
