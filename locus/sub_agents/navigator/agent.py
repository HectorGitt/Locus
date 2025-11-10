from google.adk.agents import Agent
from google.adk.tools import AgentTool
from locus.sub_agents.search.agent import search_agent
from .prompt import NAVIGATOR_PROMPT
from .tools.transport import get_local_transport
from .tools.places_search import search_places
from ...shared_libraries.model_config import get_model_type

search_tool = AgentTool(agent=search_agent)

def create_navigator_agent():
    return Agent(
        name="navigator_agent",
        model=get_model_type("sub_agent"),
        instruction=NAVIGATOR_PROMPT,
        description="Plans and optimizes routes with local transport options and place finding for comprehensive travel navigation.",
        tools=[
            get_local_transport,
            search_places,
            search_tool,
        ],
    )


navigator_agent = create_navigator_agent()
