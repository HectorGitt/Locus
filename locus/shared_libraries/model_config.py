import os


def get_model_type(agent_type: str = "sub_agent") -> str:
    """
    Gets the model type from environment variables based on agent type.

    Args:
        agent_type: Type of agent - "main" for root agent, "sub_agent" for sub-agents

    Returns:
        str: The model type to use for the specified agent type.
             - Main agent uses MODEL_TYPE_MAIN (defaults to "gemini-2.5-flash-native-audio-preview-09-2025" for live)
             - Sub-agents use MODEL_TYPE_SUB (defaults to "gemini-2.5-flash")

    """
    if agent_type == "main":
        return os.getenv("MODEL_TYPE_MAIN", "gemini-2.5-flash")
    else:  # sub_agent
        return os.getenv(
            "MODEL_TYPE_SUB", "gemini-2.5-flash-native-audio-preview-09-2025"
        )
