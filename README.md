# Locus: AI Travel Ecosystem

Locus is a multi-agent AI travel assistant built with Google Agent Development Kit (ADK). It provides comprehensive travel planning and assistance through specialized sub-agents that handle different aspects of travel.

## Features

-   **Multi-Agent Architecture**: Modular design with specialized sub-agents
-   **Flight Planning**: Find flights between destinations using Google Search
-   **Local Transport**: Get public transit and transportation options using Google Maps
-   **Weather & Climate**: Real-time weather forecasts and air quality monitoring
-   **Environmental Safety**: Air quality assessment, environmental hazards, and travel warnings
-   **Language Support**: Real-time translation services
-   **Experience Suggestions**: Local attractions and activities
-   **Outfit Planning**: Wardrobe recommendations for travel and events
-   **Web Search**: Professional search capabilities for information and research

## Architecture

### Root Agent

The main Locus agent acts as a router, delegating tasks to appropriate sub-agents based on user queries.

### Sub-Agents

-   **Navigator**: Handles flight booking and local transportation
-   **Weather**: Provides real-time weather forecasts and air quality monitoring
-   **Environmental Hazards**: Assesses environmental safety, air quality, and travel warnings
-   **Language**: Offers translation services
-   **Explorer**: Suggests local experiences and attractions
-   **Wardrobe**: Provides outfit recommendations from digital wardrobe database
-   **Search**: Professional web search and information retrieval

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
    - **Model Type**: Choose your preferred AI model (default: "gemini-2.0-flash-exp")
    - **Google Maps API Key**: For transportation, geocoding, and places data
    - **Google Cloud Translation API Key**: For language translation
    - **Google Air Quality API Key**: For real-time air quality monitoring
    - **Google Weather API Key**: For weather forecasts and conditions
    - **Google Timezone API Key**: For timezone information
    - **Google Cloud Vision API Key**: For image analysis (optional)

3. Update `.env` with your actual API keys:

    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    MODEL_TYPE=gemini-2.0-flash-exp
    GOOGLE_MAPS_API_KEY=your_maps_api_key_here
    GOOGLE_CLOUD_TRANSLATION_API_KEY=your_translation_api_key_here
    GOOGLE_AIR_QUALITY_API_KEY=your_air_quality_api_key_here
    GOOGLE_WEATHER_API_KEY=your_weather_api_key_here
    GOOGLE_TIMEZONE_API_KEY=your_timezone_api_key_here
    GOOGLE_CLOUD_VISION_API_KEY=your_vision_api_key_here

    # Wardrobe Database Configuration
    WARDROBE_DB_HOST=your_postgres_host
    WARDROBE_DB_NAME=your_wardrobe_database_name
    WARDROBE_DB_USER=your_database_username
    WARDROBE_DB_PASSWORD=your_database_password
    WARDROBE_DB_PORT=5432
    ```

### Google Custom Search Engine Setup

No longer required - search functionality is handled through the built-in Google Search tool in the Search Agent.

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

**Planning a trip with weather check**:

```
User: I'm going to San Francisco from New York. What's the weather like?

Assistant: Let me check the current weather and air quality for San Francisco.

[Agent provides weather forecast and air quality information]
```

**Environmental safety assessment**:

```
User: Is it safe to visit Beijing right now?

Assistant: Let me check air quality, environmental hazards, and travel warnings for Beijing.

[Agent provides air quality index, pollution levels, and safety advisories]
```

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

**Experience suggestions**:

```
User: What should I do in San Francisco?

Assistant: Let me suggest some local experiences and attractions.

[Agent provides activity recommendations and local insights]
```

**Outfit planning**:

```
User: What should I wear for a business meeting in Tokyo?

Assistant: Let me check your wardrobe for appropriate business attire for Tokyo weather.

[Agent provides clothing item recommendations from digital wardrobe database with details like brand, color, size, and suggests combinations]
```

## Development

```
Locus/
├── locus/
│   ├── __init__.py
│   ├── agent.py              # Root agent definition
│   ├── main.py               # Terminal interface
│   ├── prompt.py             # Router prompts
│   ├── shared_libraries/     # Shared utility functions
│   │   ├── __init__.py
│   │   ├── geocoding.py      # Shared geocoding utility
│   │   └── model_config.py   # Shared model configuration
│   └── sub_agents/
│       ├── navigator/
│       │   ├── agent.py
│       │   └── tools/
│       │       ├── places_search.py
│       │       └── transport.py
│       ├── weather/
│       │   ├── agent.py
│       │   ├── prompt.py
│       │   └── tools/
│       │       └── weather.py
│       ├── env_hazards/
│       │   ├── agent.py
│       │   ├── prompt.py
│       │   └── tools/
│       │       └── air_quality.py
│       ├── language/
│       │   ├── agent.py
│       │   ├── prompt.py
│       │   └── tools/
│       │       ├── translator.py
│       │       ├── phrasebook.py
│       │       └── speech_translator.py
│       ├── explorer/
│       │   ├── agent.py
│       │   └── tools/
│       │       └── places_search.py
│       ├── wardrobe/
│       │   ├── __init__.py
│       │   └── agent.py
│       └── search/
│           ├── agent.py
│           └── __init__.py
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
-   **Google Maps Platform**: Transportation, geocoding, and places data
-   **Google Air Quality API**: Real-time air quality monitoring and pollution data
-   **Google Weather API**: Current weather conditions and forecasts
-   **Google Search**: Built-in web search capabilities (via ADK)
-   **Google Cloud Translation**: Language translation services
-   **Google Places API**: Local attractions and experiences
-   **Google Timezone API**: Timezone information for travel planning
-   **PostgreSQL**: Digital wardrobe database for outfit recommendations

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
