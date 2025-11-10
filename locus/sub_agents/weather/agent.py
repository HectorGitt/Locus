from google.adk.agents import Agent
from google.adk.tools import AgentTool
from locus.sub_agents.search.agent import search_agent
from .prompt import WEATHER_PROMPT
from .tools.weather import get_weather
from ...shared_libraries.model_config import get_model_type

search_tool = AgentTool(agent=search_agent)

weather_agent = Agent(
    name="weather_agent",
    model=get_model_type("sub_agent"),
    instruction=WEATHER_PROMPT,
    description="Provides weather information and forecasts to help with travel planning and safety.",
    tools=[get_weather, search_tool],
)
