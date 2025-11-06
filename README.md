# Locus: AI Travel Ecosystem

Locus is a multi-agent AI travel assistant built with Google Agent Development Kit (ADK). It provides comprehensive travel planning and assistance through specialized sub-agents that handle different aspects of travel.

## Features

-   **Multi-Agent Architecture**: Modular design with specialized sub-agents
-   **Flight Planning**: Find flights between destinations using Google Custom Search
-   **Local Transport**: Get public transit and transportation options using Google Maps
-   **Budget Management**: Currency conversion and budget planning
-   **Cultural & Food Recommendations**: Local cuisine and cultural insights
-   **Language Support**: Real-time translation services
-   **Safety Information**: Travel safety alerts and advisories
-   **Experience Suggestions**: Local attractions and activities
-   **Memory System**: Context-aware conversation history

## Architecture

### Root Agent

The main Locus agent acts as a router, delegating tasks to appropriate sub-agents based on user queries.

### Sub-Agents

-   **Navigator**: Handles flight booking and local transportation
-   **Budget**: Manages currency conversion and travel budgets
-   **Culture & Food**: Provides local food and cultural recommendations
-   **Language**: Offers translation services
-   **Safety**: Delivers travel safety information
-   **Explorer**: Suggests local experiences and attractions
-   **Memory**: Maintains conversation context and history

## Prerequisites

-   Python 3.9+
-   Google Cloud account with API keys
-   Virtual environment (recommended)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/HectorGitt/Locus.git
    cd Locus
    ```

2. **Create and activate virtual environment**:

    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

### API Keys Setup

1. Copy the environment template:

    ```bash
    cp .env.example .env
    ```

2. Obtain the following API keys from Google Cloud Console:

    - **Google AI Studio API Key**: For Gemini model access
    - **Google Maps API Key**: For transportation and places data
    - **Google Custom Search API Key**: For flight search functionality
    - **Google Custom Search Engine ID**: Create a CSE at https://cse.google.com/
    - **Google Cloud Translation API Key**: For language translation
    - **Additional keys**: For vision, air quality, weather, timezone APIs

3. Update `.env` with your actual API keys:
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    GOOGLE_MAPS_API_KEY=your_maps_api_key_here
    GOOGLE_CUSTOM_SEARCH_API_KEY=your_custom_search_api_key_here
    GOOGLE_CUSTOM_SEARCH_CSE_ID=your_custom_search_engine_id_here
    GOOGLE_CLOUD_TRANSLATION_API_KEY=your_translation_api_key_here
    # ... other keys as needed
    ```

### Google Custom Search Engine Setup

1. Go to [Google Custom Search Engine](https://cse.google.com/)
2. Create a new search engine
3. Set "Sites to search" to "Search the entire web"
4. Copy the Search engine ID to your `.env` file

## Usage

### Web Interface (Recommended)

1. Start the ADK web server:

    ```bash
    adk web
    ```

2. Open your browser to `http://localhost:8000`

3. Select "locus" from the agent dropdown

4. Start chatting with your travel assistant!

### Terminal Interface

Run the agent directly in terminal:

```bash
python locus/main.py
```

## Example Interactions

**Planning a trip**:

```
User: I'm going to San Francisco from New York. How can you help?

Assistant: I can help you plan your trip! Let me find flights and local transportation options.

[Agent finds flights and provides transport suggestions]
```

**Local transport**:

```
User: How do I get from the airport to downtown San Francisco?

Assistant: I can provide public transit options using Google Maps Directions API.

[Agent provides transit routes and walking directions]
```

**Cultural recommendations**:

```
User: What should I eat in San Francisco?

Assistant: Let me suggest some local food options and cultural experiences.

[Agent provides restaurant recommendations and cultural insights]
```

## Development

### Project Structure

```
Locus/
├── locus/
│   ├── __init__.py
│   ├── agent.py              # Root agent definition
│   ├── main.py               # Terminal interface
│   ├── prompt.py             # Router prompts
│   └── sub_agents/
│       ├── navigator/
│       │   ├── agent.py
│       │   └── tools/
│       │       ├── flight_finder.py
│       │       └── transport.py
│       ├── budget/
│       ├── culture_food/
│       ├── language/
│       ├── safety/
│       ├── explorer/
│       └── memory/
├── .env                      # Environment variables
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Poetry configuration
└── README.md               # This file
```

### Adding New Tools

1. Create a new tool function in the appropriate sub-agent's `tools/` directory
2. Update the sub-agent's `agent.py` to include the new tool
3. Ensure proper error handling and API key management

### Testing

Run tests:

```bash
pytest
```

## APIs Used

-   **Google Agent Development Kit (ADK)**: Multi-agent framework
-   **Google Gemini**: AI model for natural language processing
-   **Google Maps Platform**: Transportation and places data
-   **Google Custom Search**: Flight information search
-   **Google Cloud Translation**: Language translation services
-   **Google Places API**: Local attractions and experiences

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

-   Open an issue on GitHub
-   Check the ADK documentation
-   Review Google Cloud API documentation

---

Built with ❤️ using Google Agent Development Kit
