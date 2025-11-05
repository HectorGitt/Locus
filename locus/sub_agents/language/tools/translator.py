def translate(text: str, target_language: str) -> dict:
    """
    Translates text.

    Args:
        text (str): The text to translate.
        target_language (str): The language to translate to.

    Returns:
        dict: A dictionary containing the translated text.
    """
    return {
        "translated_text": f"'{text}' in {target_language} is '{text}' (mock translation)."
    }
