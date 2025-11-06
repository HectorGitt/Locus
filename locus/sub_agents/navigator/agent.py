from google.adk.agents import Agent
from .prompt import NAVIGATOR_PROMPT
from .tools.flight_finder import find_flights
from .tools.transport import get_local_transport
from .tools.location_search import search_location

navigator_agent = Agent(
    name="navigator_agent",
    model="gemini-2.5-flash",
    instruction=NAVIGATOR_PROMPT,
    description="Plans and optimizes your route, including flight finder, local transport guide, offline navigation, and real-time re-routing.",
    tools=[find_flights, get_local_transport, search_location],
)
