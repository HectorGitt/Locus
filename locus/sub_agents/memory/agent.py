from google.adk.agents import Agent
from .prompt import MEMORY_PROMPT
from .tools.memory_saver import save_memory
from ...shared_libraries.model_config import get_model_type

memory_agent = Agent(
    name="memory_agent",
    model=get_model_type(),
    instruction=MEMORY_PROMPT,
    description="Records and summarizes your journey, including an auto journal, highlights, expense log, and a 'memories map'.",
    tools=[save_memory],
)
