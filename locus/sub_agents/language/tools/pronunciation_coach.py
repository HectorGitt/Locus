import os
import requests
from typing import Optional


def pronunciation_coach(text: str, target_language: Optional[str] = None) -> dict:
    """
    Provides pronunciation guidance and coaching for foreign language phrases.

    Args:
        text (str): The text to provide pronunciation guidance for.
        target_language (str, optional): The target language for pronunciation.

    Returns:
        dict: Pronunciation guidance and tips.
    """
    api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
    search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_CSE_ID")

    if not api_key or not search_engine_id:
        return {
            "error": "GOOGLE_CUSTOM_SEARCH_API_KEY or GOOGLE_CUSTOM_SEARCH_CSE_ID not found in .env file."
        }

    # Search for pronunciation guides
    query = f'"{text}" pronunciation guide'
    if target_language:
        query += f" {target_language}"

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

        # Generate phonetic breakdown
        phonetic_guide = generate_phonetic_breakdown(text, target_language)

        return {
            "original_text": text,
            "target_language": target_language or "detected",
            "phonetic_breakdown": phonetic_guide,
            "pronunciation_resources": results[:3],  # Top 3 results
            "practice_tips": get_practice_tips(text, target_language),
        }

    except Exception as e:
        return {"error": f"Failed to get pronunciation guidance: {str(e)}"}


def generate_phonetic_breakdown(text: str, language: Optional[str] = None) -> dict:
    """
    Generates a phonetic breakdown of the text.

    Args:
        text (str): Text to break down phonetically.
        language (str, optional): Target language.

    Returns:
        dict: Phonetic breakdown information.
    """
    words = text.split()

    # This is a simplified phonetic guide - in production you'd use proper phonetic libraries
    phonetic_mapping = {
        # Common English sounds
        "th": "θ/ð",
        "ch": "tʃ",
        "sh": "ʃ",
        "ph": "f",
        "wh": "w/h",
        "ee": "iː",
        "oo": "uː",
        "ou": "aʊ",
        "oi": "ɔɪ",
        "ea": "iː",
        # Common foreign sounds that English speakers struggle with
        "ñ": "ɲ",
        "ü": "y",
        "ç": "s/ts",
        "ğ": "ɣ",
        "ş": "ʃ",
    }

    breakdown = []
    for word in words:
        word_lower = word.lower()
        challenging_sounds = []

        for sound, ipa in phonetic_mapping.items():
            if sound in word_lower:
                challenging_sounds.append(f"{sound} → {ipa}")

        breakdown.append(
            {
                "word": word,
                "syllables": estimate_syllables(word),
                "stress_pattern": estimate_stress(word),
                "challenging_sounds": challenging_sounds,
                "simplified_pronunciation": simplify_pronunciation(word),
            }
        )

    return {
        "word_breakdown": breakdown,
        "overall_difficulty": assess_difficulty(text),
        "language_specific_notes": get_language_pronunciation_notes(language),
    }


def estimate_syllables(word: str) -> list:
    """
    Estimates syllable breakdown for a word.

    Args:
        word (str): Word to break into syllables.

    Returns:
        list: Syllable breakdown.
    """
    # Simplified syllable estimation
    vowels = "aeiouy"
    syllables = []
    current_syllable = ""

    for char in word.lower():
        current_syllable += char
        if char in vowels:
            # Check for vowel clusters and consonant boundaries
            if len(current_syllable) > 1:
                syllables.append(current_syllable)
                current_syllable = ""

    if current_syllable:
        syllables.append(current_syllable)

    return syllables if syllables else [word]


def estimate_stress(word: str) -> str:
    """
    Estimates stress pattern for English words.

    Args:
        word (str): Word to analyze.

    Returns:
        str: Stress pattern description.
    """
    word_lower = word.lower()

    # Basic stress rules for English
    if len(word) <= 3:
        return "First syllable stressed"
    elif word_lower.endswith(("tion", "sion", "ic", "ical", "ity", "ty")):
        return "Third-to-last syllable stressed"
    elif word_lower.endswith(("ate", "ise", "ize", "ive", "ing")):
        return "Second-to-last syllable stressed"
    else:
        return "First syllable typically stressed"


def simplify_pronunciation(word: str) -> str:
    """
    Creates a simplified pronunciation guide.

    Args:
        word (str): Word to simplify.

    Returns:
        str: Simplified pronunciation.
    """
    # Replace common tricky sounds with easier approximations
    simplified = word.lower()
    simplified = simplified.replace("th", "th(z)")
    simplified = simplified.replace("ch", "ch")
    simplified = simplified.replace("sh", "sh")
    simplified = simplified.replace("ph", "f")
    simplified = simplified.replace("wh", "w")

    return f"Approximately: {simplified}"


def assess_difficulty(text: str) -> str:
    """
    Assesses overall pronunciation difficulty.

    Args:
        text (str): Text to assess.

    Returns:
        str: Difficulty level.
    """
    text_lower = text.lower()

    # Count challenging elements
    challenging_elements = [
        "th",
        "ch",
        "sh",
        "ph",
        "wh",
        "r",
        "v",
        "w",
        "z",
        "j",
        "ñ",
        "ü",
        "ç",
        "ğ",
        "ş",
        "ø",
        "å",
        "æ",
    ]

    challenge_count = sum(
        1 for element in challenging_elements if element in text_lower
    )

    if challenge_count == 0:
        return "Easy"
    elif challenge_count <= 2:
        return "Moderate"
    else:
        return "Challenging"


def get_language_pronunciation_notes(language: Optional[str] = None) -> list:
    """
    Provides language-specific pronunciation notes.

    Args:
        language (str, optional): Target language.

    Returns:
        list: Pronunciation tips for the language.
    """
    language_tips = {
        "french": [
            "French 'r' is made in the throat, not the tongue",
            "Many final consonants are silent",
            "Liaison: connect words ending/starting with vowels",
            "Nasal vowels: an, en, in, on, un",
        ],
        "spanish": [
            "Roll your 'rr' and 'r' sounds",
            "H is always silent",
            "B/V sound the same (like B)",
            "Double L sounds like 'y' in 'yes'",
        ],
        "german": [
            "CH can sound like 'k' or 'sh' depending on context",
            "W sounds like English 'v'",
            "Ü, Ö, Ä have no English equivalent",
            "R can be rolled or throaty",
        ],
        "japanese": [
            "Practice long and short vowels carefully",
            "R/L sound is midway between both",
            "Double consonants are held longer",
            "Pitch accent affects meaning",
        ],
        "italian": [
            "C/K before I/E sounds like 'ch'",
            "G before I/E sounds like 'j'",
            "R is rolled, especially between vowels",
            "Double consonants are emphasized",
        ],
    }

    if language and language.lower() in language_tips:
        return language_tips[language.lower()]

    return [
        "Listen to native speakers",
        "Practice with a language exchange partner",
        "Use pronunciation apps and videos",
        "Record yourself and compare with natives",
        "Break words into syllables when learning",
    ]


def get_practice_tips(text: str, language: Optional[str] = None) -> list:
    """
    Provides practice tips for the given text.

    Args:
        text (str): Text to practice.
        language (str, optional): Target language.

    Returns:
        list: Practice tips.
    """
    tips = [
        "Repeat the phrase 5-10 times slowly",
        "Record yourself and listen for improvement",
        "Break it into smaller chunks if it's long",
        "Practice in front of a mirror to watch mouth movements",
        "Say it faster each time you repeat it",
    ]

    # Add language-specific tips
    if language:
        language_specific = {
            "french": "Practice the French 'r' by gargling gently",
            "spanish": "Practice rolling R's by trilling your tongue",
            "german": "Practice the 'ch' sound by saying 'k' + 'sh'",
            "japanese": "Focus on pitch differences between similar words",
            "italian": "Practice the musical rhythm of Italian speech",
        }

        if language.lower() in language_specific:
            tips.append(language_specific[language.lower()])

    return tips
