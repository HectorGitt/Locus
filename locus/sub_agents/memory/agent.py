from google.adk.agents import Agent
from .prompt import MEMORY_PROMPT
from .tools.memory_saver import save_memory

memory_agent = Agent(
    name="memory_agent",
    model="gemini-2.0-flash",
    instruction=MEMORY_PROMPT,
    description="Records and summarizes your journey, including an auto journal, highlights, expense log, and a 'memories map'.",
    tools=[save_memory],
)
