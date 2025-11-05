def get_safety_alerts(location: str) -> dict:
    """
    Gets safety alerts for a location.

    Args:
        location (str): The location to get safety alerts for.

    Returns:
        dict: A dictionary containing safety alerts.
    """
    return {
        "safety_alerts": f"It is generally safe in {location}, but be aware of your surroundings."
    }
