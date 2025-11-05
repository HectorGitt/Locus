def suggest_experiences(mood: str = None, weather: str = None) -> dict:
    """
    Suggests experiences based on mood or weather.

    Args:
        mood (str, optional): The user's current mood (e.g., "adventurous", "relaxed").
        weather (str, optional): The current weather (e.g., "sunny", "rainy").

    Returns:
        dict: A dictionary containing a list of suggested experiences.
    """
    if mood == "adventurous":
        return {
            "experiences": ["Go hiking in the nearby mountains.", "Try rock climbing."]
        }
    elif mood == "relaxed":
        return {"experiences": ["Visit a quiet park.", "Find a cozy cafe."]}
    elif weather == "sunny":
        return {"experiences": ["Go to the beach.", "Have a picnic."]}
    elif weather == "rainy":
        return {"experiences": ["Visit a museum.", "Go to the cinema."]}
    else:
        return {
            "experiences": [
                "I'm not sure what to suggest. Can you tell me more about what you're looking for?"
            ]
        }
