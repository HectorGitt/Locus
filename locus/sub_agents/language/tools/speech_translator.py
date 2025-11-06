import os
import requests
from typing import Optional


def speech_translation_guide(
    source_language: str, target_language: str, context: Optional[str] = None
) -> dict:
    """
    Provides guidance for real-time speech translation and communication.

    Args:
        source_language (str): Source language code (e.g., 'en').
        target_language (str): Target language code (e.g., 'es').
        context (str, optional): Communication context (e.g., 'restaurant', 'emergency').

    Returns:
        dict: Speech translation guidance and tips.
    """
    api_key = os.getenv("GOOGLE_CLOUD_TRANSLATION_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_CLOUD_TRANSLATION_API_KEY not found in .env file."}

    # Get common phrases for the context
    common_phrases = get_common_phrases(context or "general", source_language)

    # Translate key phrases
    translated_phrases = []
    for phrase in common_phrases[:10]:  # Limit to 10 phrases
        translation = translate_phrase(phrase, target_language, api_key)
        if translation:
            translated_phrases.append(
                {
                    "source": phrase,
                    "target": translation["translated_text"],
                    "pronunciation": generate_simple_pronunciation(
                        translation["translated_text"]
                    ),
                }
            )

    return {
        "language_pair": f"{source_language} → {target_language}",
        "context": context or "general",
        "essential_phrases": translated_phrases,
        "communication_tips": get_speech_translation_tips(
            source_language, target_language
        ),
        "apps_recommendations": get_translation_apps(),
        "emergency_phrases": get_emergency_phrases(
            source_language, target_language, api_key
        ),
    }


def get_common_phrases(context: str, language: str) -> list:
    """
    Gets common phrases for a specific context and language.

    Args:
        context (str): Communication context.
        language (str): Language code.

    Returns:
        list: Common phrases for the context.
    """
    phrases_by_context = {
        "restaurant": [
            "Menu please",
            "I would like...",
            "Water please",
            "The bill please",
            "I'm allergic to...",
            "That tastes good",
            "Check please",
            "Bathroom?",
        ],
        "transportation": [
            "Where is the train station?",
            "How much is a ticket to...?",
            "When does the bus leave?",
            "I need to go to...",
            "Taxi please",
        ],
        "hotel": [
            "I have a reservation",
            "Check-in please",
            "Where is my room?",
            "Room service please",
            "Checkout time?",
            "WiFi password?",
        ],
        "shopping": [
            "How much is this?",
            "Do you have this in...?",
            "Can I try this on?",
            "I would like to return this",
            "Do you accept cards?",
        ],
        "emergency": [
            "Help!",
            "I need a doctor",
            "Call the police",
            "Where is the hospital?",
            "I've lost my wallet",
            "I don't speak the language",
        ],
        "general": [
            "Hello",
            "Thank you",
            "Please",
            "Excuse me",
            "I'm sorry",
            "How much?",
            "Where is...?",
            "What time is it?",
            "Yes",
            "No",
        ],
    }

    return phrases_by_context.get(context.lower(), phrases_by_context["general"])


def translate_phrase(text: str, target_language: str, api_key: str) -> Optional[dict]:
    """
    Translates a phrase using Google Translate API.

    Args:
        text (str): Text to translate.
        target_language (str): Target language code.
        api_key (str): Google Cloud API key.

    Returns:
        dict: Translation result or None.
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
            "source_language": translation.get("detectedSourceLanguage", "auto"),
        }
    except Exception:
        return None


def generate_simple_pronunciation(text: str) -> str:
    """
    Generates a simple pronunciation guide.

    Args:
        text (str): Text to create pronunciation guide for.

    Returns:
        str: Simple pronunciation guide.
    """
    # Basic pronunciation guide - in production use proper phonetic libraries
    return f"Listen to: {text} (use Google Translate for accurate audio)"


def get_speech_translation_tips(source_lang: str, target_lang: str) -> list:
    """
    Provides tips for speech translation between languages.

    Args:
        source_lang (str): Source language code.
        target_lang (str): Target language code.

    Returns:
        list: Communication tips.
    """
    general_tips = [
        "Speak slowly and clearly when using translation apps",
        "Use simple sentences for better translation accuracy",
        "Point and use gestures to supplement translation",
        "Have key phrases written down as backup",
        "Learn numbers and common words in advance",
    ]

    # Language-specific tips
    language_pairs = {
        ("en", "es"): [
            "English speakers: Roll your 'rr' sounds",
            "Spanish speakers: English 'h' is silent",
            "Practice 'j' sound - like Scottish 'loch'",
        ],
        ("en", "fr"): [
            "English speakers: French 'r' comes from throat",
            "French speakers: English 'th' sound doesn't exist - use 'z' or 's'",
            "Practice French nasal vowels",
        ],
        ("en", "de"): [
            "English speakers: German 'ch' is throaty",
            "German speakers: English 'w' sounds like 'v'",
            "Practice German umlauts: ü, ö, ä",
        ],
        ("en", "ja"): [
            "English speakers: Japanese has no 'l' or 'v' sounds",
            "Japanese speakers: English 'r' is different - practice tongue position",
            "Pay attention to pitch accent",
        ],
    }

    pair = (source_lang.lower(), target_lang.lower())
    reverse_pair = (target_lang.lower(), source_lang.lower())

    if pair in language_pairs:
        return general_tips + language_pairs[pair]
    elif reverse_pair in language_pairs:
        return general_tips + language_pairs[reverse_pair]
    else:
        return general_tips


def get_translation_apps() -> list:
    """
    Recommends translation apps for travelers.

    Returns:
        list: App recommendations with features.
    """
    return [
        {
            "name": "Google Translate",
            "features": [
                "Real-time camera translation",
                "Offline translation",
                "Voice translation",
            ],
            "best_for": "Quick translations, camera text recognition",
        },
        {
            "name": "Microsoft Translator",
            "features": ["Conversation mode", "Offline packs", "Multiple languages"],
            "best_for": "Real-time conversations, business travel",
        },
        {
            "name": "iTranslate",
            "features": ["Voice translation", "Phrasebook", "Offline mode"],
            "best_for": "Voice input, comprehensive phrasebooks",
        },
        {
            "name": "Papago",
            "features": ["Korean expertise", "Camera translation", "Voice"],
            "best_for": "Travel to Korea, Asian languages",
        },
    ]


def get_emergency_phrases(source_lang: str, target_lang: str, api_key: str) -> list:
    """
    Gets emergency phrases translated between languages.

    Args:
        source_lang (str): Source language code.
        target_lang (str): Target language code.
        api_key (str): Google Cloud API key.

    Returns:
        list: Emergency phrases with translations.
    """
    emergency_phrases = [
        "Help!",
        "I need a doctor",
        "Call the police",
        "Where is the hospital?",
        "I've been robbed",
        "I lost my passport",
        "I don't speak the language",
        "I need medicine",
        "I'm allergic to...",
        "Fire!",
    ]

    translated_emergencies = []
    for phrase in emergency_phrases:
        translation = translate_phrase(phrase, target_lang, api_key)
        if translation:
            translated_emergencies.append(
                {
                    "english": phrase,
                    "translated": translation["translated_text"],
                    "priority": "high",
                }
            )

    return translated_emergencies
