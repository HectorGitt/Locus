from google.adk.agents import Agent
from .prompt import SAFETY_PROMPT
from ...shared_libraries.model_config import get_model_type

safety_agent = Agent(
    name="safety_agent",
    model=get_model_type(),
    instruction=SAFETY_PROMPT,
    description="Protects and informs with local laws, health advisories, and scam/risk detection.",
    tools=[],
)
