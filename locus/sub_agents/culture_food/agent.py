from google.adk.agents import Agent
from .prompt import CULTURE_FOOD_PROMPT
from .tools.food_suggester import suggest_street_food
from ...shared_libraries.model_config import get_model_type

culture_food_agent = Agent(
    name="culture_food_agent",
    model=get_model_type(),
    instruction=CULTURE_FOOD_PROMPT,
    description="Teaches you local culture, including etiquette guide, street food suggestions, what to avoid, and dining safety.",
    tools=[suggest_street_food],
)
