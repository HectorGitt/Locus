import os
import googlemaps
from typing import Optional


def search_places(query: str, location: Optional[str] = None) -> dict:
    """
    Searches for places using Google Places API.

    Args:
        query (str): The search query for places (e.g., "YC office", "restaurants").
        location (str, optional): The location to search around (e.g., "San Francisco, CA").

    Returns:
        dict: A dictionary containing place search results.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY not found in .env file."}

    gmaps = googlemaps.Client(key=api_key)

    try:
        # Use Places API text search
        places_result = gmaps.places(
            query=query, location=location, radius=50000
        )  # 50km radius

        results = []
        for place in places_result.get("results", []):
            result = {
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "location": place.get("geometry", {}).get("location"),
                "place_id": place.get("place_id"),
                "rating": place.get("rating"),
                "types": place.get("types", []),
            }
            results.append(result)

        return {"places": results}

    except Exception as e:
        return {"error": str(e)}
