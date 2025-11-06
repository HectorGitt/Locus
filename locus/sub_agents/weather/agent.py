from google.adk.agents import Agent
from .prompt import WEATHER_PROMPT
from .tools.weather import get_weather
from ..env_hazards.tools.air_quality import check_air_quality
from ...shared_libraries.model_config import get_model_type

weather_agent = Agent(
    name="weather_agent",
    model=get_model_type(),
    instruction=WEATHER_PROMPT,
    description="Provides weather information and forecasts to help with travel planning and safety.",
    tools=[get_weather, check_air_quality],
)
