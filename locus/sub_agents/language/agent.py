from google.adk.agents import Agent
from .prompt import LANGUAGE_PROMPT
from .tools.translator import translate_text

language_agent = Agent(
    name="language_agent",
    model="gemini-2.5-flash",
    instruction=LANGUAGE_PROMPT,
    description="Helps you communicate, with a phrasebook generator, AI speech translator, slang detector, and pronunciation coach.",
    tools=[translate_text],
)
