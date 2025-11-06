from google.adk.agents import Agent
from .prompt import BUDGET_PROMPT
from .tools.currency_converter import convert_currency
from ...shared_libraries.model_config import get_model_type

budget_agent = Agent(
    name="budget_agent",
    model=get_model_type(),
    instruction=BUDGET_PROMPT,
    description="Manages and predicts expenses, including currency converter, local cost of living calculator, and daily budget tracker.",
    tools=[convert_currency],
)
