from google.adk.agents import Agent
from .prompt import ENV_HAZARDS_PROMPT
from .tools.air_quality import check_air_quality
from ...shared_libraries.model_config import get_model_type

env_hazards_agent = Agent(
    name="env_hazards_agent",
    model=get_model_type("sub_agent"),
    instruction=ENV_HAZARDS_PROMPT,
    description="Assesses environmental safety and air quality for travel destinations.",
    tools=[check_air_quality],
)
