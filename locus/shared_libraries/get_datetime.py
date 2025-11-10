"""
Shared utility for getting current datetime information.
This ensures consistent date/time context across all agents.
"""

from datetime import datetime


def get_current_datetime() -> dict:
    """
    Get comprehensive current datetime information.
    
    Returns:
        dict: Dictionary containing various datetime formats
    """
    now = datetime.now()
    
    return {
        "datetime_obj": now,
        "date": now.strftime("%B %d, %Y"),  # e.g., "November 10, 2025"
        "day": now.strftime("%A"),  # e.g., "Monday"
        "short_date": now.strftime("%Y-%m-%d"),  # e.g., "2025-11-10"
        "time": now.strftime("%H:%M:%S"),  # e.g., "14:30:45"
        "time_12h": now.strftime("%I:%M %p"),  # e.g., "02:30 PM"
        "year": now.year,
        "month": now.month,
        "month_name": now.strftime("%B"),
        "day_of_month": now.day,
        "day_of_week": now.strftime("%A"),
        "timestamp": int(now.timestamp()),
    }


def get_datetime_string() -> str:
    """
    Get a formatted datetime string for prompts.
    
    Returns:
        str: Formatted string like "Today is November 10, 2025 (Monday)"
    """
    dt = get_current_datetime()
    return f"Today is {dt['date']} ({dt['day']})"


def get_prompt_datetime_context() -> str:
    """
    Get datetime context suitable for agent prompts.
    
    Returns:
        str: Multi-line datetime context for prompts
    """
    dt = get_current_datetime()
    return f"""Current Date Context: Today is {dt['date']} ({dt['day']}). Use this to interpret relative dates like "tomorrow", "next week", or day names like "Saturday"."""
