import os
import requests
from locus.shared_libraries.geocoding import geocode_location


def check_air_quality(location: str) -> dict:
    """
    Checks air quality index and pollution levels for a location using Google Air Quality API.

    Args:
        location (str): The city or location to check air quality for.

    Returns:
        dict: A dictionary containing air quality information.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY not found in .env file."}

    try:
        # Geocode the location using shared utility
        geocode_result = geocode_location(location)
        if "error" in geocode_result:
            return {"error": geocode_result["error"]}

        lat = geocode_result["lat"]
        lng = geocode_result["lng"]

        # Use Google Air Quality API
        air_quality_url = (
            "https://airquality.googleapis.com/v1/currentConditions:lookup"
        )
        # Use POST with JSON body as required by the API
        air_quality_payload = {"location": {"latitude": lat, "longitude": lng}}
        air_quality_params = {"key": api_key}

        air_quality_response = requests.post(
            air_quality_url,
            params=air_quality_params,
            json=air_quality_payload,
            headers={"Content-Type": "application/json"},
        )
        air_quality_response.raise_for_status()
        air_quality_data = air_quality_response.json()

        if "error" in air_quality_data:
            raise Exception(
                f"Air Quality API error: {air_quality_data['error']['message']}"
            )

        # Parse air quality data
        indexes = air_quality_data.get("indexes", [])
        pollutants = air_quality_data.get("pollutants", [])

        if not indexes:
            raise Exception("No air quality data available for this location.")

        # Get the main AQI index (usually AQI)
        main_index = None
        for index in indexes:
            if index.get("code") == "uaqi":
                main_index = index
                break
        if not main_index:
            main_index = indexes[0]  # Use first available index

        # Get pollutant details
        pollutant_details = []
        for pollutant in pollutants[:5]:  # Limit to top 5 pollutants
            pollutant_details.append(
                {
                    "code": pollutant.get("code"),
                    "display_name": pollutant.get("displayName"),
                    "full_name": pollutant.get("fullName"),
                    "concentration_value": pollutant.get("concentration", {}).get(
                        "value"
                    ),
                    "concentration_units": pollutant.get("concentration", {}).get(
                        "units"
                    ),
                }
            )

        return {
            "location": location,
            "coordinates": {"lat": lat, "lng": lng},
            "air_quality": {
                "index": main_index.get("code"),
                "display_name": main_index.get("displayName"),
                "aqi_value": main_index.get("aqi"),
                "aqi_display": main_index.get("aqiDisplay"),
                "category": main_index.get("category"),
                "dominant_pollutant": main_index.get("dominantPollutant"),
            },
            "pollutants": pollutant_details,
            "date_time": air_quality_data.get("dateTime"),
            "source": "Google Air Quality API",
        }

    except Exception as e:
        return {"error": f"Failed to fetch air quality information: {str(e)}"}
