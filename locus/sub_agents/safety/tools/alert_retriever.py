import os
from googleapiclient.discovery import build


def get_safety_alerts(location: str) -> dict:
    """
    Gets safety alerts for a location using Google Custom Search API.

    Args:
        location (str): The location to get safety alerts for.

    Returns:
        dict: A dictionary containing safety alerts.
    """
    api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
    cse_id = os.getenv("GOOGLE_CUSTOM_SEARCH_CSE_ID")
    if not api_key or not cse_id:
        return {
            "error": "GOOGLE_CUSTOM_SEARCH_API_KEY or GOOGLE_CUSTOM_SEARCH_CSE_ID not found in .env file."
        }

    service = build("customsearch", "v1", developerKey=api_key)

    query = f"travel advisory {location} site:travel.state.gov OR site:gov.uk"

    try:
        result = service.cse().list(q=query, cx=cse_id, num=3).execute()
        if "items" in result and result["items"]:
            alerts = []
            for item in result["items"]:
                alerts.append(
                    {
                        "title": item.get("title", ""),
                        "snippet": item.get("snippet", ""),
                        "link": item.get("link", ""),
                    }
                )
            return {"safety_alerts": alerts}
        else:
            return {
                "message": f"No specific safety alerts found for {location}. Always check official sources."
            }
    except Exception as e:
        return {"error": str(e)}
