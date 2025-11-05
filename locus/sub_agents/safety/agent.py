from google.adk.agents import Agent
from .prompt import SAFETY_PROMPT
from .tools.alert_retriever import get_safety_alerts

safety_agent = Agent(
    name="safety_agent",
    model="gemini-2.5-flash",
    instruction=SAFETY_PROMPT,
    description="Protects and informs with safety alerts, local laws, health advisories, and scam/risk detection.",
    tools=[get_safety_alerts],
)
