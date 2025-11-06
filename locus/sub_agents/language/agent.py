from google.adk.agents import Agent
from .prompt import LANGUAGE_PROMPT
from .tools.translator import translate_text
from .tools.phrasebook import generate_phrasebook
from .tools.slang_detector import detect_slang, explain_communication_norm
from .tools.pronunciation_coach import pronunciation_coach
from .tools.speech_translator import speech_translation_guide

language_agent = Agent(
    name="language_agent",
    model="gemini-2.5-flash",
    instruction=LANGUAGE_PROMPT,
    description="Helps you communicate, with a phrasebook generator, AI speech translator, slang detector, and pronunciation coach.",
    tools=[
        translate_text,
        generate_phrasebook,
        detect_slang,
        explain_communication_norm,
        pronunciation_coach,
        speech_translation_guide,
    ],
)
