from google.adk.agents import Agent
from google.adk.tools import AgentTool
from dotenv import load_dotenv
from .prompt import ROUTER_PROMPT
from locus.sub_agents.navigator.agent import navigator_agent
from locus.sub_agents.weather.agent import weather_agent
from locus.sub_agents.env_hazards.agent import env_hazards_agent
from locus.sub_agents.language.agent import language_agent
from locus.sub_agents.explorer.agent import explorer_agent
from locus.sub_agents.search.agent import search_agent
from locus.sub_agents.wardrobe.agent import wardrobe_agent
from .shared_libraries.model_config import get_model_type

# Load environment variables from .env file
load_dotenv()

# Create AgentTool instances for each sub-agent
navigator_tool = AgentTool(agent=navigator_agent)
weather_tool = AgentTool(agent=weather_agent)
env_hazards_tool = AgentTool(agent=env_hazards_agent)
language_tool = AgentTool(agent=language_agent)
explorer_tool = AgentTool(agent=explorer_agent)
search_tool = AgentTool(agent=search_agent)
wardrobe_tool = AgentTool(agent=wardrobe_agent)

root_agent = Agent(
    name="locus",
    model=get_model_type("main"),
    instruction=ROUTER_PROMPT,
    description="Comprehensive AI travel assistant coordinating specialized agents for weather, navigation, safety, culture, language, budget, exploration, and wardrobe planning.",
    tools=[
        navigator_tool,
        weather_tool,
        env_hazards_tool,
        language_tool,
        explorer_tool,
        search_tool,
        wardrobe_tool,
    ],
)
