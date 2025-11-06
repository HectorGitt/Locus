from google.adk.agents import Agent
from .prompt import NAVIGATOR_PROMPT
from .tools.flight_finder import find_flights
from .tools.flight_prices import find_flight_prices
from .tools.transport import get_local_transport
from .tools.location_search import search_location
from .tools.places_search import search_places

navigator_agent = Agent(
    name="navigator_agent",
    model="gemini-2.5-flash",
    instruction=NAVIGATOR_PROMPT,
    description="Plans and optimizes your route, including flight finder, local transport guide, offline navigation, and real-time re-routing.",
    tools=[
        find_flights,
        find_flight_prices,
        get_local_transport,
        search_location,
        search_places,
    ],
)
