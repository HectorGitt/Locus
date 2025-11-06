from google.adk.agents import Agent
from .prompt import EXPLORER_PROMPT
from .tools.suggestions import suggest_experiences

explorer_agent = Agent(
    name="explorer_agent",
    model="gemini-2.0-flash",
    instruction=EXPLORER_PROMPT,
    description="Suggests experiences, hidden spots, and events based on mood or weather.",
    tools=[suggest_experiences],
)
