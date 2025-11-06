import os
import requests
from typing import Optional


def detect_slang(text: str, context: Optional[str] = None) -> dict:
    """
    Detects slang, idioms, and informal expressions in text and provides explanations.

    Args:
        text (str): The text to analyze for slang.
        context (str, optional): Cultural context or region for more accurate detection.

    Returns:
        dict: Analysis of slang and informal expressions found.
    """
    api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_CSE_ID")

    if not api_key or not search_engine_id:
        return {
            "error": "GOOGLE_CUSTOM_SEARCH_API_KEY or GOOGLE_CUSTOM_SEARCH_CSE_ID not found in .env file."
        }

    # Search for slang explanations
    query = f'"{text}" slang meaning urban dictionary'
    if context:
        query += f" {context}"

    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": query,
            "num": 5,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("items", []):
            result = {
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": item.get("link"),
            }
            results.append(result)

        # Analyze if the text contains potential slang
        slang_indicators = analyze_slang_indicators(text)

        return {
            "original_text": text,
            "slang_analysis": slang_indicators,
            "explanations": results[:3],  # Top 3 results
            "cultural_context": get_cultural_context(text, context),
        }

    except Exception as e:
        return {"error": f"Failed to analyze slang: {str(e)}"}


def analyze_slang_indicators(text: str) -> dict:
    """
    Analyzes text for potential slang indicators.

    Args:
        text (str): Text to analyze.

    Returns:
        dict: Analysis of slang indicators.
    """
    words = text.lower().split()

    # Common slang patterns (this is a simplified version)
    slang_patterns = {
        "informal_contractions": ["ain't", "gonna", "wanna", "gotta", "lemme", "gimme"],
        "internet_slang": ["lol", "brb", "smh", "idk", "tbh", "imo", "yolo", "fomo"],
        "emphasis_words": ["super", "totally", "literally", "absolutely", "definitely"],
        "slang_suffixes": ["-ish", "-like", "-esque", "-tastic"],
    }

    found_indicators = {
        "informal_contractions": [
            word for word in words if word in slang_patterns["informal_contractions"]
        ],
        "internet_slang": [
            word for word in words if word in slang_patterns["internet_slang"]
        ],
        "emphasis_words": [
            word for word in words if word in slang_patterns["emphasis_words"]
        ],
        "slang_suffixes": [
            word
            for word in words
            if any(word.endswith(suffix) for suffix in slang_patterns["slang_suffixes"])
        ],
    }

    has_slang = any(found_indicators.values())

    return {
        "contains_potential_slang": has_slang,
        "indicators_found": found_indicators,
        "formality_level": "informal" if has_slang else "neutral",
    }


def get_cultural_context(text: str, context: Optional[str] = None) -> dict:
    """
    Provides cultural context for communication styles.

    Args:
        text (str): The text being analyzed.
        context (str, optional): Cultural or regional context.

    Returns:
        dict: Cultural communication insights.
    """
    # Basic cultural communication guidance
    communication_styles = {
        "american": {
            "style": "Direct and informal",
            "tips": [
                "Use first names quickly",
                "Small talk is common",
                "Humor and sarcasm are appreciated",
            ],
            "taboos": [
                "Avoid politics at first meeting",
                "Don't ask about salary or age",
            ],
        },
        "british": {
            "style": "Polite and indirect",
            "tips": [
                "Use 'please' and 'thank you'",
                "Weather is safe small talk",
                "Self-deprecation is common",
            ],
            "taboos": ["Avoid boasting", "Don't discuss money openly"],
        },
        "japanese": {
            "style": "Formal and indirect",
            "tips": [
                "Use honorifics",
                "Silence can be comfortable",
                "Group harmony is important",
            ],
            "taboos": ["Avoid direct confrontation", "Don't blow nose in public"],
        },
        "german": {
            "style": "Direct and efficient",
            "tips": [
                "Be punctual",
                "Structure conversations logically",
                "Direct questions are normal",
            ],
            "taboos": ["Avoid small talk initially", "Don't interrupt"],
        },
    }

    if context and context.lower() in communication_styles:
        return communication_styles[context.lower()]

    # Default to general tips
    return {
        "style": "Varies by culture",
        "general_tips": [
            "Observe local communication patterns",
            "When in doubt, be polite and respectful",
            "Learn basic local greetings",
            "Pay attention to personal space and touch norms",
            "Consider formality levels in different situations",
        ],
    }


def explain_communication_norm(text: str, culture: str) -> dict:
    """
    Explains communication norms and expectations in different cultures.

    Args:
        text (str): Example text or scenario.
        culture (str): Target culture.

    Returns:
        dict: Cultural communication guidance.
    """
    api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_CSE_ID")

    if not api_key or not search_engine_id:
        return {
            "error": "GOOGLE_CUSTOM_SEARCH_API_KEY or GOOGLE_CUSTOM_SEARCH_CSE_ID not found in .env file."
        }

    query = f"{culture} culture communication norms etiquette"

    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": query,
            "num": 3,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("items", []):
            result = {
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": item.get("link"),
            }
            results.append(result)

        return {
            "culture": culture,
            "communication_norms": results,
            "example_context": text,
        }

    except Exception as e:
        return {"error": f"Failed to get cultural communication norms: {str(e)}"}
