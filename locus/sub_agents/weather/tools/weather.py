import os
import requests
from typing import Optional
from datetime import datetime, timedelta


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
        # First, geocode the location using Google Maps Geocoding API
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        geocode_params = {"address": location, "key": api_key}

        geocode_response = requests.get(geocode_url, params=geocode_params)
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()

        if not geocode_data.get("results"):
            return {"error": f"Could not find location: {location}"}

        lat = geocode_data["results"][0]["geometry"]["location"]["lat"]
        lng = geocode_data["results"][0]["geometry"]["location"]["lng"]

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

    # Parse current conditions
    conditions = weather_data.get("currentConditions", {})

    return {
        "location": location,
        "coordinates": {"lat": lat, "lng": lng},
        "date": datetime.now().strftime("%Y-%m-%d"),
        "current_weather": {
            "temperature_celsius": conditions.get("temperature", {}).get("degrees"),
            "temperature_fahrenheit": celsius_to_fahrenheit(
                conditions.get("temperature", {}).get("degrees")
            ),
            "feels_like_celsius": conditions.get("temperature", {}).get("heatIndex"),
            "humidity_percent": conditions.get("relativeHumidity"),
            "wind_speed_mps": conditions.get("wind", {}).get("speed", {}).get("value")
            if conditions.get("wind")
            else None,
            "wind_direction_degrees": conditions.get("wind", {})
            .get("direction", {})
            .get("degrees")
            if conditions.get("wind")
            else None,
            "description": conditions.get("conditions", {}).get("localizedDescription"),
            "main_condition": conditions.get("conditions", {}).get("description"),
            "precipitation_probability": conditions.get("precipitation", {}).get(
                "probability"
            )
            * 100
            if conditions.get("precipitation")
            else 0,
            "cloudiness_percent": conditions.get("cloudCover", {}).get("percentage")
            if conditions.get("cloudCover")
            else None,
            "uv_index": conditions.get("uvIndex"),
            "visibility_meters": conditions.get("visibility", {}).get("value")
            if conditions.get("visibility")
            else None,
        },
    }


def get_forecast_weather(
    lat: float, lng: float, api_key: str, location: str, days_ahead: int
) -> dict:
    """Get weather forecast using Google Maps Weather API."""
    weather_url = "https://weather.googleapis.com/v1/forecast:lookup"
    weather_params = {
        "key": api_key,
        "location.latitude": lat,
        "location.longitude": lng,
        "days": min(days_ahead + 1, 10),  # API supports up to 10 days
    }

    weather_response = requests.get(weather_url, params=weather_params)
    weather_response.raise_for_status()
    weather_data = weather_response.json()

    if "error" in weather_data:
        return {"error": f"Weather API error: {weather_data['error']['message']}"}

    # Find forecast for the requested day
    forecasts = weather_data.get("forecast", {}).get("days", [])
    if not forecasts or len(forecasts) <= days_ahead:
        return {"error": f"No forecast available for {days_ahead} days ahead"}

    target_forecast = forecasts[days_ahead]
    target_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    return {
        "location": location,
        "coordinates": {"lat": lat, "lng": lng},
        "forecast_date": target_date,
        "days_ahead": days_ahead,
        "forecast": {
            "temperature_celsius": target_forecast.get("temperature", {}).get(
                "degrees"
            ),
            "temperature_fahrenheit": celsius_to_fahrenheit(
                target_forecast.get("temperature", {}).get("degrees")
            ),
            "min_temp_celsius": target_forecast.get("temperature", {}).get("min"),
            "max_temp_celsius": target_forecast.get("temperature", {}).get("max"),
            "min_temp_fahrenheit": celsius_to_fahrenheit(
                target_forecast.get("temperature", {}).get("min")
            ),
            "max_temp_fahrenheit": celsius_to_fahrenheit(
                target_forecast.get("temperature", {}).get("max")
            ),
            "humidity_percent": target_forecast.get("relativeHumidity"),
            "description": target_forecast.get("conditions", {}).get(
                "localizedDescription"
            ),
            "main_condition": target_forecast.get("conditions", {}).get("description"),
            "precipitation_probability": target_forecast.get("precipitation", {}).get(
                "probability"
            )
            * 100
            if target_forecast.get("precipitation")
            else 0,
            "wind_speed_mps": target_forecast.get("wind", {})
            .get("speed", {})
            .get("value")
            if target_forecast.get("wind")
            else None,
            "wind_direction_degrees": target_forecast.get("wind", {})
            .get("direction", {})
            .get("degrees")
            if target_forecast.get("wind")
            else None,
            "uv_index": target_forecast.get("uvIndex"),
            "sunrise": target_forecast.get("sunrise"),
            "sunset": target_forecast.get("sunset"),
        },
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
