import os
import googlemaps
from datetime import datetime


def get_local_transport(destination: str, origin: str = "") -> dict:
    """
    Provides local transport information using Google Maps Directions API.

    Args:
        destination (str): The destination address or landmark.
        origin (str, optional): The starting address. If not provided,
                                it will search for public transit routes.

    Returns:
        dict: A dictionary containing transport information.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY not found in .env file."}

    gmaps = googlemaps.Client(key=api_key)

    if not origin:
        # If no origin is specified, find public transit stations near the destination
        try:
            geocode_result = gmaps.geocode(destination)
            if not geocode_result:
                return {"error": f"Could not find location: {destination}"}

            lat = geocode_result[0]["geometry"]["location"]["lat"]
            lng = geocode_result[0]["geometry"]["location"]["lng"]

            places_result = gmaps.places_nearby(
                location=(lat, lng), radius=1000, type="transit_station"
            )

            stations = [place["name"] for place in places_result.get("results", [])]
            if not stations:
                return {
                    "message": f"No major public transport stations found near {destination}."
                }

            return {"transit_stations_nearby": stations}

        except Exception as e:
            return {"error": str(e)}

    try:
        now = datetime.now()
        directions_result = gmaps.directions(
            origin, destination, mode="transit", departure_time=now
        )
        return directions_result
    except Exception as e:
        return {"error": str(e)}
