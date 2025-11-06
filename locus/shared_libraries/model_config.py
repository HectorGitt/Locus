import os


def get_model_type() -> str:
    """
    Gets the model type from environment variables.

    Returns:
        str: The model type to use for agents (defaults to "gemini-2.5-flash" if not set).

    Example:
        >>> model = get_model_type()
        >>> print(model)
        "gemini-2.5-flash"
    """
    return os.getenv("MODEL_TYPE", "gemini-2.5-flash")
