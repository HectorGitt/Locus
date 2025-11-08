from google.adk.agents import Agent
from .prompt import NAVIGATOR_PROMPT
from .tools.transport import get_local_transport
from .tools.places_search import search_places
from ...shared_libraries.model_config import get_model_type


def create_navigator_agent():
    return Agent(
        name="navigator_agent",
        model=get_model_type(),
        instruction=NAVIGATOR_PROMPT,
        description="Plans and optimizes routes with local transport options and place finding for comprehensive travel navigation.",
        tools=[
            get_local_transport,
            search_places,
        ],
    )


navigator_agent = create_navigator_agent()
