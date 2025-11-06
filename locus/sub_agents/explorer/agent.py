from google.adk.agents import Agent
from .prompt import EXPLORER_PROMPT
from .tools.suggestions import suggest_experiences
from ...shared_libraries.model_config import get_model_type

explorer_agent = Agent(
    name="explorer_agent",
    model=get_model_type(),
    instruction=EXPLORER_PROMPT,
    description="Suggests experiences, hidden spots, and events based on mood or weather.",
    tools=[suggest_experiences],
)
