import os
import requests
from typing import Optional


def generate_phrasebook(destination: str, context: Optional[str] = None) -> dict:
    """
    Generates a customized phrasebook for travelers based on destination and context.

    Args:
        destination (str): The travel destination (city/country).
        context (str, optional): Specific context like "restaurant", "transportation", "emergency", etc.

    Returns:
        dict: A dictionary containing categorized phrases with translations and pronunciations.
    """
    api_key = os.getenv("GOOGLE_CLOUD_TRANSLATION_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_CLOUD_TRANSLATION_API_KEY not found in .env file."}

    # Define essential phrase categories
    categories = {
        "greetings": [
            "Hello",
            "Good morning",
            "Good afternoon",
            "Good evening",
            "Goodbye",
            "How are you?",
            "I'm fine, thank you",
            "What's your name?",
            "My name is...",
        ],
        "transportation": [
            "Where is the airport?",
            "How do I get to...?",
            "How much does it cost?",
            "A taxi please",
            "Train station",
            "Bus stop",
            "I need a ticket to...",
        ],
        "restaurant": [
            "Menu please",
            "I would like...",
            "The bill please",
            "Water please",
            "I'm vegetarian",
            "That tastes good",
            "Check please",
        ],
        "emergency": [
            "Help!",
            "I need a doctor",
            "Call the police",
            "Where is the hospital?",
            "I've lost my passport",
            "I don't understand",
            "Please speak slowly",
        ],
        "shopping": [
            "How much is this?",
            "Do you have...?",
            "Can I try this on?",
            "I would like to return this",
            "Do you accept credit cards?",
        ],
    }

    # Filter categories based on context
    if context and context.lower() in categories:
        selected_categories = {context.lower(): categories[context.lower()]}
    else:
        # Default to essential categories
        selected_categories = {
            "greetings": categories["greetings"],
            "transportation": categories["transportation"],
            "restaurant": categories["restaurant"],
            "emergency": categories["emergency"],
        }

    # Get local language for destination
    local_language = get_destination_language(destination)
    if not local_language:
        return {"error": f"Could not determine primary language for {destination}"}

    phrasebook = {}

    for category, phrases in selected_categories.items():
        translated_phrases = []
        for phrase in phrases:
            translation = translate_phrase(phrase, local_language, api_key)
            if translation:
                translated_phrases.append(
                    {
                        "english": phrase,
                        "local": translation["translated_text"],
                        "pronunciation": generate_pronunciation_guide(
                            translation["translated_text"]
                        ),
                    }
                )

        phrasebook[category] = translated_phrases

    return {
        "destination": destination,
        "local_language": local_language,
        "phrasebook": phrasebook,
        "cultural_tips": get_cultural_tips(destination),
    }


def get_destination_language(destination: str) -> Optional[str]:
    """
    Determines the primary language spoken at a destination.

    Args:
        destination (str): The destination location.

    Returns:
        str: Language code (e.g., 'es', 'fr', 'de') or None if not found.
    """
    # Simple mapping of major destinations to languages
    language_map = {
        # European countries
        "france": "fr",
        "paris": "fr",
        "spain": "es",
        "madrid": "es",
        "barcelona": "es",
        "germany": "de",
        "berlin": "de",
        "munich": "de",
        "italy": "it",
        "rome": "it",
        "venice": "it",
        "florence": "it",
        "uk": "en",
        "london": "en",
        "england": "en",
        "netherlands": "nl",
        "amsterdam": "nl",
        "belgium": "nl",
        "brussels": "nl",
        # Asian countries
        "japan": "ja",
        "tokyo": "ja",
        "kyoto": "ja",
        "china": "zh",
        "beijing": "zh",
        "shanghai": "zh",
        "thailand": "th",
        "bangkok": "th",
        "vietnam": "vi",
        "hanoi": "vi",
        "korea": "ko",
        "seoul": "ko",
        "india": "hi",
        "delhi": "hi",
        "mumbai": "hi",
        # Americas
        "mexico": "es",
        "mexico city": "es",
        "brazil": "pt",
        "rio": "pt",
        "sao paulo": "pt",
        "argentina": "es",
        "buenos aires": "es",
        "canada": "en",
        "toronto": "en",
        "vancouver": "en",
        # Middle East/Africa
        "egypt": "ar",
        "cairo": "ar",
        "morocco": "ar",
        "casablanca": "ar",
        "turkey": "tr",
        "istanbul": "tr",
        "israel": "he",
        "tel aviv": "he",
        "saudi arabia": "ar",
        "riyadh": "ar",
    }

    destination_lower = destination.lower()
    return language_map.get(destination_lower)


def translate_phrase(text: str, target_language: str, api_key: str) -> Optional[dict]:
    """
    Translates a single phrase using Google Translate API.

    Args:
        text (str): Text to translate.
        target_language (str): Target language code.
        api_key (str): Google Cloud API key.

    Returns:
        dict: Translation result or None if failed.
    """
    try:
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {"q": text, "target": target_language, "key": api_key}

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        translation = data["data"]["translations"][0]
        return {
            "translated_text": translation["translatedText"],
            "source_language": translation.get("detectedSourceLanguage", "en"),
        }
    except Exception:
        return None


def generate_pronunciation_guide(text: str) -> str:
    """
    Generates a simple pronunciation guide for foreign text.

    Args:
        text (str): Text to create pronunciation guide for.

    Returns:
        str: Simplified pronunciation guide.
    """
    # This is a basic implementation - in a real system you'd use proper phonetic libraries
    # For now, just return the text with some basic guidance
    return f"Listen to audio pronunciation or use Google Translate for accurate phonetics: {text}"


def get_cultural_tips(destination: str) -> list:
    """
    Provides cultural communication tips for the destination.

    Args:
        destination (str): The destination location.

    Returns:
        list: List of cultural communication tips.
    """
    # Basic cultural tips - could be expanded with more comprehensive data
    general_tips = [
        "Learn basic greetings - they're appreciated even if you struggle with the language",
        "Use please/thank you - politeness goes a long way",
        "Pointing and gestures can help when words fail",
        "Download translation apps for real-time help",
        "Learn numbers 1-10 for prices and addresses",
    ]

    return general_tips
