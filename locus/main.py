import asyncio
import os

from dotenv import load_dotenv
from google.adk.runtime import Runner, Session
from google.adk.agents.services import InMemorySessionService

from locus.agent import root_agent


async def main():
    """Run the main agent."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")

    runner = Runner(
        agent=root_agent,
        session_service=InMemorySessionService(),
        api_key=api_key,
    )

    session_id = "test-session"
    session = Session(id=session_id)

    print("Welcome to Locus! How can I help you plan your next adventure?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = await runner.run(session, user_input)
        print(f"Locus: {response.output}")


if __name__ == "__main__":
    asyncio.run(main())
