from google.adk.agents import Agent
from .prompt import CULTURE_FOOD_PROMPT
from .tools.food_suggester import suggest_food

culture_food_agent = Agent(
    name="culture_food_agent",
    model="gemini-2.5-flash",
    instruction=CULTURE_FOOD_PROMPT,
    description="Teaches you local culture, including etiquette guide, street food suggestions, what to avoid, and dining safety.",
    tools=[suggest_food],
)
