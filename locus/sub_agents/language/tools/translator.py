import os
import requests


def translate_text(text: str, target_language: str) -> dict:
    """
    Translates text using Google Cloud Translation API.

    Args:
        text (str): The text to translate.
        target_language (str): The language code to translate to (e.g., 'es' for Spanish).

    Returns:
        dict: A dictionary containing the translated text.
    """
    api_key = os.getenv("GOOGLE_CLOUD_TRANSLATION_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_CLOUD_TRANSLATION_API_KEY not found in .env file."}

    url = "https://translation.googleapis.com/language/translate/v2"
    params = {"q": text, "target": target_language, "key": api_key}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        translation = data["data"]["translations"][0]
        return {
            "translated_text": translation["translatedText"],
            "source_language": translation.get("detectedSourceLanguage", "Unknown"),
        }
    except Exception as e:
        return {"error": str(e)}
