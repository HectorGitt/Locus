from google.adk.agents import Agent
from google.adk.tools import AgentTool
from .prompt import EXPLORER_PROMPT
from .tools.suggestions import suggest_experiences
from ..search.agent import search_agent
from ...shared_libraries.model_config import get_model_type

# Create search agent tool
search_tool = AgentTool(agent=search_agent)

explorer_agent = Agent(
    name="explorer_agent",
    model=get_model_type("sub_agent"),
    instruction=EXPLORER_PROMPT,
    description="Suggests experiences, attractions, and activities based on user preferences, travel context, and current conditions.",
    tools=[suggest_experiences, search_tool],
)
