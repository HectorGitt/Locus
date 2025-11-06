import os
import requests


def check_air_quality(location: str) -> dict:
    """
    Checks air quality index and pollution levels for a location using Google Air Quality API with fallback to search.

    Args:
        location (str): The city or location to check air quality for.

    Returns:
        dict: A dictionary containing air quality information.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY not found in .env file."}

    try:
        # First geocode the location using Google Maps Geocoding API
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        geocode_params = {"address": location, "key": api_key}

        geocode_response = requests.get(geocode_url, params=geocode_params)
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()

        if not geocode_data.get("results"):
            return {"error": f"Could not find location: {location}"}

        lat = geocode_data["results"][0]["geometry"]["location"]["lat"]
        lng = geocode_data["results"][0]["geometry"]["location"]["lng"]

        # Try Google Air Quality API first
        try:
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

        except Exception as api_error:
            # Fallback to search-based method if Google Air Quality API fails
            print(
                f"Google Air Quality API failed ({api_error}), falling back to search method"
            )

            search_api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
            search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_CSE_ID")

            if not search_api_key or not search_engine_id:
                return {
                    "error": f"Google Air Quality API failed and fallback search keys not found: {str(api_error)}"
                }

            # Search for current air quality information
            query = f"air quality index AQI {location} current today"
            search_url = "https://www.googleapis.com/customsearch/v1"
            search_params = {
                "key": search_api_key,
                "cx": search_engine_id,
                "q": query,
                "num": 3,
            }

            search_response = requests.get(search_url, params=search_params)
            search_response.raise_for_status()
            search_data = search_response.json()

            results = []
            for item in search_data.get("items", []):
                result = {
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet"),
                    "source": "Google Search (fallback)",
                }
                results.append(result)

            if not results:
                return {
                    "error": f"No air quality information found for {location}. API error: {str(api_error)}"
                }

            return {
                "location": location,
                "coordinates": {"lat": lat, "lng": lng},
                "air_quality_info": results,
                "note": "Air quality data sourced from web search (Google Air Quality API unavailable).",
                "source": "Google Search (fallback)",
            }

    except Exception as e:
        return {"error": f"Failed to fetch air quality information: {str(e)}"}


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
