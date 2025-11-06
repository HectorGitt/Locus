from google.adk.agents import Agent
from .prompt import NAVIGATOR_PROMPT
from .tools.flight_finder import find_flights
from .tools.flight_prices import find_flight_prices
from .tools.transport import get_local_transport
from .tools.location_search import search_location
from .tools.places_search import search_places
from ...shared_libraries.model_config import get_model_type

navigator_agent = Agent(
    name="navigator_agent",
    model=get_model_type(),
    instruction=NAVIGATOR_PROMPT,
    description="Plans and optimizes routes with flight price comparisons, local transport options, location search, and place finding for comprehensive travel navigation.",
    tools=[
        find_flights,
        find_flight_prices,
        get_local_transport,
        search_location,
        search_places,
    ],
)
