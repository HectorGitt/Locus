from google.adk.agents import Agent
from dotenv import load_dotenv
from .prompt import ROUTER_PROMPT
from locus.sub_agents.navigator.agent import navigator_agent
from locus.sub_agents.weather.agent import weather_agent
from locus.sub_agents.env_hazards.agent import env_hazards_agent
from locus.sub_agents.budget.agent import budget_agent
from locus.sub_agents.culture_food.agent import culture_food_agent
from locus.sub_agents.language.agent import language_agent
from locus.sub_agents.safety.agent import safety_agent
from locus.sub_agents.explorer.agent import explorer_agent
from locus.sub_agents.memory.agent import memory_agent
from .shared_libraries.model_config import get_model_type

# Load environment variables from .env file
load_dotenv()

root_agent = Agent(
    name="locus",
    model=get_model_type(),
    instruction=ROUTER_PROMPT,
    description="Comprehensive AI travel assistant coordinating specialized agents for weather, navigation, safety, culture, language, budget, exploration, and trip memory management.",
    sub_agents=[
        navigator_agent,
        weather_agent,
        env_hazards_agent,
        budget_agent,
        culture_food_agent,
        language_agent,
        safety_agent,
        explorer_agent,
        memory_agent,
    ],
)
