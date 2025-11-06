import os
import requests
from typing import Optional
from datetime import datetime, timedelta
from locus.shared_libraries.geocoding import geocode_location


def get_weather(
    location: str, days_ahead: Optional[int] = 0, specific_date: Optional[str] = None
) -> dict:
    """
    Gets weather information for a location using Google Maps Weather API.

    Args:
        location (str): The city or location to get weather for.
        days_ahead (int, optional): Number of days ahead from today (0 = today, 1 = tomorrow, etc.). Defaults to 0.
        specific_date (str, optional): Specific date in YYYY-MM-DD format for historical/past weather.

    Returns:
        dict: A dictionary containing weather information.
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

        # Use Google Maps Weather API for weather data
        if specific_date:
            # Historical weather data
            try:
                target_date = datetime.strptime(specific_date, "%Y-%m-%d")
                today = datetime.now()

                if target_date.date() == today.date():
                    # Today - use current conditions
                    return get_current_weather(lat, lng, api_key, location)
                elif target_date > today:
                    # Future date - use forecast
                    days_diff = (target_date - today).days
                    return get_forecast_weather(lat, lng, api_key, location, days_diff)
                else:
                    # Past date - use historical data
                    return get_historical_weather(
                        lat, lng, api_key, location, specific_date
                    )
            except ValueError:
                return {"error": "Invalid date format. Please use YYYY-MM-DD format."}

        elif days_ahead == 0:
            # Current weather
            return get_current_weather(lat, lng, api_key, location)
        else:
            # Forecast
            return get_forecast_weather(lat, lng, api_key, location, days_ahead)

    except Exception as e:
        return {"error": f"Failed to fetch weather information: {str(e)}"}


def get_current_weather(lat: float, lng: float, api_key: str, location: str) -> dict:
    """Get current weather conditions using Google Maps Weather API."""
    weather_url = "https://weather.googleapis.com/v1/currentConditions:lookup"
    weather_params = {
        "key": api_key,
        "location.latitude": lat,
        "location.longitude": lng,
    }

    weather_response = requests.get(weather_url, params=weather_params)
    weather_response.raise_for_status()
    weather_data = weather_response.json()

    if "error" in weather_data:
        return {"error": f"Weather API error: {weather_data['error']['message']}"}

    # Parse current conditions directly from root level
    return {
        "location": location,
        "coordinates": {"lat": lat, "lng": lng},
        "date": datetime.now().strftime("%Y-%m-%d"),
        "current_weather": {
            "temperature_celsius": weather_data.get("temperature", {}).get("degrees"),
            "temperature_fahrenheit": celsius_to_fahrenheit(
                weather_data.get("temperature", {}).get("degrees")
            ),
            "feels_like_celsius": weather_data.get("feelsLikeTemperature", {}).get(
                "degrees"
            ),
            "humidity_percent": weather_data.get("relativeHumidity"),
            "wind_speed_mps": weather_data.get("wind", {}).get("speed", {}).get("value")
            / 3.6
            if weather_data.get("wind", {}).get("speed")
            else None,  # Convert km/h to m/s
            "wind_direction_degrees": weather_data.get("wind", {})
            .get("direction", {})
            .get("degrees"),
            "description": weather_data.get("weatherCondition", {})
            .get("description", {})
            .get("text"),
            "main_condition": weather_data.get("weatherCondition", {}).get("type"),
            "precipitation_probability": weather_data.get("precipitation", {})
            .get("probability", {})
            .get("percent")
            if weather_data.get("precipitation")
            else 0,
            "cloudiness_percent": weather_data.get("cloudCover"),
            "uv_index": weather_data.get("uvIndex"),
            "visibility_meters": weather_data.get("visibility", {}).get("distance")
            * 1000
            if weather_data.get("visibility")
            else None,  # Convert km to m
            "pressure_hpa": weather_data.get("airPressure", {}).get(
                "meanSeaLevelMillibars"
            ),
            "dew_point_celsius": weather_data.get("dewPoint", {}).get("degrees"),
        },
    }


def get_forecast_weather(
    lat: float, lng: float, api_key: str, location: str, days_ahead: int
) -> dict:
    """Get weather forecast - Google Maps Weather API only provides current conditions."""
    target_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    return {
        "location": location,
        "coordinates": {"lat": lat, "lng": lng},
        "forecast_date": target_date,
        "days_ahead": days_ahead,
        "note": "Google Maps Weather API only provides current weather conditions. Forecast data is not available through this API.",
        "message": f"Unable to provide forecast for {target_date}. Consider using a dedicated weather service for future weather predictions.",
    }


def get_historical_weather(
    lat: float, lng: float, api_key: str, location: str, specific_date: str
) -> dict:
    """Get historical weather data using Google Maps Weather API."""
    weather_url = "https://weather.googleapis.com/v1/history:lookup"
    weather_params = {
        "key": api_key,
        "location.latitude": lat,
        "location.longitude": lng,
        "timestamp": specific_date + "T12:00:00Z",  # Midday timestamp
        "hours": 24,  # Get 24 hours of data
    }

    weather_response = requests.get(weather_url, params=weather_params)
    weather_response.raise_for_status()
    weather_data = weather_response.json()

    if "error" in weather_data:
        return {"error": f"Weather API error: {weather_data['error']['message']}"}

    # Parse historical data
    hours = weather_data.get("history", {}).get("hours", [])
    if not hours:
        return {"error": f"No historical data available for {specific_date}"}

    # Calculate daily aggregates
    temps = [
        h.get("temperature", {}).get("degrees") for h in hours if h.get("temperature")
    ]
    min_temp = min(temps) if temps else None
    max_temp = max(temps) if temps else None
    avg_temp = sum(temps) / len(temps) if temps else None

    # Get midday conditions (closest to noon)
    midday_hour = None
    for hour in hours:
        hour_time = hour.get("timestamp", "")
        if "12:" in hour_time or "13:" in hour_time:
            midday_hour = hour
            break
    if not midday_hour:
        midday_hour = hours[len(hours) // 2]  # Middle of available data

    return {
        "location": location,
        "coordinates": {"lat": lat, "lng": lng},
        "date": specific_date,
        "historical_weather": {
            "average_temperature_celsius": avg_temp,
            "average_temperature_fahrenheit": celsius_to_fahrenheit(avg_temp),
            "min_temp_celsius": min_temp,
            "max_temp_celsius": max_temp,
            "min_temp_fahrenheit": celsius_to_fahrenheit(min_temp),
            "max_temp_fahrenheit": celsius_to_fahrenheit(max_temp),
            "humidity_percent": midday_hour.get("relativeHumidity"),
            "description": midday_hour.get("conditions", {}).get(
                "localizedDescription"
            ),
            "main_condition": midday_hour.get("conditions", {}).get("description"),
            "precipitation_amount_mm": midday_hour.get("precipitation", {}).get(
                "amount"
            ),
            "wind_speed_mps": midday_hour.get("wind", {}).get("speed", {}).get("value")
            if midday_hour.get("wind")
            else None,
            "wind_direction_degrees": midday_hour.get("wind", {})
            .get("direction", {})
            .get("degrees")
            if midday_hour.get("wind")
            else None,
            "cloudiness_percent": midday_hour.get("cloudCover", {}).get("percentage")
            if midday_hour.get("cloudCover")
            else None,
        },
    }


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return round((celsius * 9 / 5) + 32, 1) if celsius is not None else None
