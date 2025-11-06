from google.adk.agents import Agent
from .prompt import WEATHER_PROMPT
from .tools.weather import get_weather
from ..env_hazards.tools.air_quality import check_air_quality

weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    instruction=WEATHER_PROMPT,
    description="Provides weather information and forecasts to help with travel planning and safety.",
    tools=[get_weather, check_air_quality],
)
