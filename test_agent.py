#!/usr/bin/env python3
"""
Test script for Locus agent comprehensive travel planning.
"""

import asyncio
from locus.agent import root_agent


async def test_comprehensive_query():
    """Test the agent with a comprehensive travel query."""
    query = (
        "i am going to San Francisco from ibadan, how should i move and what do i need?"
    )

    print(f"Testing query: {query}")
    print("=" * 50)

    try:
        # Run the agent with the query
        response = await root_agent.run(query)
        print("Agent Response:")
        print(response)
    except Exception as e:
        print(f"Error running agent: {e}")


if __name__ == "__main__":
    asyncio.run(test_comprehensive_query())
