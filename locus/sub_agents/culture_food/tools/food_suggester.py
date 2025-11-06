import os
import googlemaps


def suggest_street_food(location: str) -> dict:
    """
    Suggests street food for a given location using Google Places API.

    Args:
        location (str): The location to find street food.

    Returns:
        dict: A dictionary containing food suggestions.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY not found in .env file."}

    gmaps = googlemaps.Client(key=api_key)

    try:
        # Geocode the location to get coordinates
        geocode_result = gmaps.geocode(location)
        if not geocode_result:
            return {"error": f"Could not find location: {location}"}

        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lng = geocode_result[0]["geometry"]["location"]["lng"]

        # Search for places with type 'restaurant' and keyword 'street food'
        places_result = gmaps.places_nearby(
            location=(lat, lng),
            radius=5000,  # 5km radius
            type="restaurant",
            keyword="street food",
        )

        places = places_result.get("results", [])
        if not places:
            return {"message": f"No street food places found near {location}."}

        suggestions = []
        for place in places[:5]:  # Limit to 5 suggestions
            name = place.get("name", "Unknown")
            rating = place.get("rating", "N/A")
            address = place.get("vicinity", "Address not available")
            suggestions.append({"name": name, "rating": rating, "address": address})

        return {"street_food_suggestions": suggestions}

    except Exception as e:
        return {"error": str(e)}
