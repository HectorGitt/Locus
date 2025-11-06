import os
import re
from googleapiclient.discovery import build


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """
    Converts currency using Google Custom Search API.

    Args:
        amount (float): The amount to convert.
        from_currency (str): The currency to convert from.
        to_currency (str): The currency to convert to.

    Returns:
        dict: A dictionary containing the converted amount.
    """
    api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
    cse_id = os.getenv(
        "GOOGLE_CUSTOM_SEARCH_CSE_ID"
    )  # You'll need to create a Custom Search Engine
    if not api_key or not cse_id:
        return {
            "error": "GOOGLE_CUSTOM_SEARCH_API_KEY or GOOGLE_CUSTOM_SEARCH_CSE_ID not found in .env file."
        }

    service = build("customsearch", "v1", developerKey=api_key)

    query = f"1 {from_currency} to {to_currency} exchange rate"

    try:
        result = service.cse().list(q=query, cx=cse_id, num=1).execute()
        if "items" in result and result["items"]:
            snippet = result["items"][0]["snippet"]
            # Parse the exchange rate from the snippet
            match = re.search(
                r"1\s*"
                + re.escape(from_currency)
                + r"\s*=\s*([\d.]+)\s*"
                + re.escape(to_currency),
                snippet,
                re.IGNORECASE,
            )
            if match:
                rate = float(match.group(1))
                converted = amount * rate
                return {
                    "converted_amount": f"{amount} {from_currency} = {converted:.2f} {to_currency}",
                    "exchange_rate": f"1 {from_currency} = {rate} {to_currency}",
                }
            else:
                return {"error": "Could not parse exchange rate from search results."}
        else:
            return {"error": "No search results found."}
    except Exception as e:
        return {"error": str(e)}
