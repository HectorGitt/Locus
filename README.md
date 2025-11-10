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
    - **Model Types**: Configure model types for main agent and sub-agents
    - **Google Maps API Key**: For Maps Platform services (geocoding, directions, places, weather, air quality, and timezone)
    - **Google Cloud Translation API Key**: For language translation
    - **Google Cloud Vision API Key**: For image analysis (optional)

3. Update `.env` with your actual API keys:

    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    MODEL_TYPE_MAIN=gemini-2.0-flash-exp
    MODEL_TYPE_SUB=gemini-2.5-flash
    GOOGLE_MAPS_API_KEY=your_maps_api_key_here
    GOOGLE_CLOUD_TRANSLATION_API_KEY=your_translation_api_key_here
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
-   **Google Maps Platform**: Single API key for multiple services including:
    -   Maps API: Transportation routing and directions
    -   Geocoding API: Location coordinate conversion
    -   Places API: Local attractions and points of interest
    -   Weather API: Current weather conditions and forecasts
    -   Air Quality API: Real-time air quality monitoring and pollution data
    -   Timezone API: Timezone information
-   **Google Search**: Built-in web search capabilities (via ADK)
-   **Google Cloud Translation**: Language translation services
-   **PostgreSQL**: Digital wardrobe database for outfit recommendations

## Challenges Faced

During the development of Locus, we encountered and overcame several significant challenges:

### Database Integration Challenges

-   **Password Authentication Issues**: Initial database connection failures due to incorrect password configuration and PostgreSQL authentication restrictions
-   **Schema Evolution**: Adapting the wardrobe database schema to match simplified requirements while maintaining backward compatibility
-   **Connection Management**: Implementing proper database session handling and connection pooling for multi-agent operations

### Multi-Agent Coordination

-   **Waiting Message Duplication**: Initial implementation showed waiting messages twice during comprehensive guide generation due to redundant instructions in the agent prompt
-   **Agent Call Sequencing**: Coordinating multiple sub-agents to work together seamlessly for comprehensive travel guides without user interruption
-   **Response Synchronization**: Ensuring all agent responses are collected before providing final synthesized recommendations

### Code Architecture and Organization

-   **Code Duplication**: Eliminating repetitive database operations, error handling, and item formatting across multiple functions
-   **Modular Refactoring**: Restructuring the wardrobe agent by moving database utilities and CRUD operations into separate tool files for better maintainability
-   **Import Management**: Properly organizing imports and dependencies across the modular architecture

### API Integration Complexities

-   **Multiple Google APIs**: Coordinating various Google Cloud services (Maps, Weather, Air Quality, Translation, Search) with proper error handling
-   **Rate Limiting**: Managing API call frequencies and implementing fallback mechanisms for service outages
-   **Authentication Management**: Securely handling multiple API keys and environment configurations

### Development Workflow

-   **Testing Multi-Agent Systems**: Developing comprehensive test strategies for interdependent agent interactions
-   **Error Propagation**: Ensuring meaningful error messages bubble up correctly through the agent hierarchy
-   **Performance Optimization**: Balancing response times with comprehensive information gathering

### Solutions Implemented

-   **Helper Functions**: Created reusable database utilities (`get_db()`, `close_db()`, `item_to_dict()`, `handle_db_error()`) to eliminate code duplication
-   **Modular Tools**: Organized database operations into separate tool files (`db_utils.py`, `query_tools.py`, `crud_tools.py`)
-   **Streamlined Prompts**: Consolidated waiting message instructions to prevent duplication while maintaining clear user communication
-   **Robust Error Handling**: Implemented consistent error response formats across all agent operations
-   **Environment Validation**: Added database connection testing utilities to verify configuration before deployment

These challenges helped us build a more robust, maintainable, and user-friendly multi-agent travel assistant.

## Deployment

Locus can be deployed to Google Cloud Run using the provided PowerShell deployment script. The deployment process uses Google Cloud Build to containerize the application.

### Prerequisites for Deployment

-   **Google Cloud SDK**: Install and configure `gcloud` CLI
-   **Docker**: Required for local builds (optional if using Cloud Build)
-   **Google Cloud Project**: Active GCP project with billing enabled
-   **Required APIs Enabled**:
    -   Cloud Run API
    -   Cloud Build API
    -   Artifact Registry API
    -   Secret Manager API

### Deployment Options

#### Option 1: Automated Deployment (Recommended)

Use the provided PowerShell deployment script:

```powershell
.\deploy.ps1
```

**What it does:**

-   Configures Python environment for gcloud
-   Sets model types (main agent: `gemini-2.5-flash-native-audio-preview-09-2025`, sub-agents: `gemini-2.0-flash`)
-   Creates temporary deployment folder
-   Generates Dockerfile automatically
-   Builds and deploys to Cloud Run with UI
-   Cleans up temporary files

**Configuration:**
The script automatically configures:

-   Project ID: `pivotal-equinox-472613-d3`
-   Region: `us-central1`
-   Service Name: `locus-agent-service`
-   Port: `8000`

#### Option 2: Manual Deployment

1. **Create secrets for sensitive data:**

```powershell
.\create-secrets.ps1
```

This creates Google Cloud secrets for:

-   API keys (Gemini, Google Maps, Translation, Custom Search)
-   Database credentials (host, name, user, password, port)

2. **Grant service account access to secrets:**

```powershell
.\grant-secret-access.ps1
```

3. **Deploy using ADK CLI:**

```bash
adk deploy cloud_run \
  --project=YOUR_PROJECT_ID \
  --region=us-central1 \
  --service_name=locus-agent-service \
  --with_ui \
  ./locus
```

#### Option 3: Manual gcloud Deployment

```bash
gcloud run deploy locus-agent-service \
  --source ./locus \
  --platform managed \
  --region us-central1 \
  --project YOUR_PROJECT_ID \
  --allow-unauthenticated
```

### Deployment Scripts

#### `deploy.ps1`

Main deployment script with:

-   Automatic Python environment configuration
-   Model type environment variables
-   Custom temp folder management
-   Error handling and status reporting

#### `create-secrets.ps1`

Creates Google Cloud secrets for:

-   `GEMINI_API_KEY`
-   `GOOGLE_API_KEY`
-   `GOOGLE_MAPS_API_KEY`
-   `GOOGLE_CUSTOM_SEARCH_API_KEY`
-   `GOOGLE_CUSTOM_SEARCH_CSE_ID`
-   `GOOGLE_CLOUD_TRANSLATION_API_KEY`
-   `WARDROBE_DB_HOST`
-   `WARDROBE_DB_NAME`
-   `WARDROBE_DB_USER`
-   `WARDROBE_DB_PASSWORD`
-   `WARDROBE_DB_PORT`

#### `grant-secret-access.ps1`

Grants IAM policy bindings for Cloud Run service account to access all secrets.

### Deployment Challenges and Solutions

#### Challenge 1: Docker Daemon Not Running

**Error:** `[WinError 2] The system cannot find the file specified`

**Solution:**

-   Start Docker Desktop before deployment
-   Or use Cloud Build (remote building) instead of local Docker

#### Challenge 2: gcloud Python Module Issues

**Error:** `No module named 'grpc'`

**Solution:**
Configure gcloud to use venv Python:

```powershell
$env:CLOUDSDK_PYTHON = ".\venv\Scripts\python.exe"
```

This is now automatically handled in `deploy.ps1`.

#### Challenge 3: Windows Path Issues with subprocess

**Error:** Command execution failures on Windows

**Solution:**

-   Added `shell=True` to subprocess.run calls
-   Fixed path handling for Windows PowerShell
-   Used absolute paths for temp folders

#### Challenge 4: Temp Folder Permissions

**Error:** Access denied or path too long errors

**Solution:**

-   Changed from system temp directory to project-relative `.\deployment\temp`
-   Proper cleanup in finally block
-   Created deployment folder structure

### Post-Deployment

After successful deployment:

1. **Access your deployed service:**

    ```
    https://locus-agent-service-[PROJECT-ID].us-central1.run.app
    ```

2. **Configure secrets access** (if not already done):

    ```powershell
    .\grant-secret-access.ps1
    ```

3. **Test the deployment:**

    - Open the service URL in your browser
    - Interact with the Locus agent through the UI
    - Verify all sub-agents are responding correctly

4. **Monitor logs:**
    ```bash
    gcloud run logs read locus-agent-service --project=YOUR_PROJECT_ID
    ```

### Environment Variables in Cloud Run

The deployment automatically sets:

-   `MODEL_TYPE_MAIN`: gemini-2.5-flash-native-audio-preview-09-2025
-   `MODEL_TYPE_SUB`: gemini-2.0-flash
-   `GOOGLE_CLOUD_PROJECT`: Your GCP project ID
-   `GOOGLE_CLOUD_LOCATION`: us-central1

Secrets are mounted as environment variables via Secret Manager.

### Cost Optimization

To minimize Cloud Run costs:

-   Set minimum instances to 0 (scale to zero when idle)
-   Use appropriate memory/CPU limits
-   Enable request-based autoscaling
-   Monitor and optimize cold start times

### Troubleshooting Deployment

**Issue: Build fails**

-   Check Dockerfile generation in temp folder
-   Verify requirements.txt includes all dependencies
-   Ensure Python 3.11+ compatibility

**Issue: Runtime errors**

-   Verify all secrets are created and accessible
-   Check Cloud Run logs for detailed error messages
-   Ensure database connectivity from Cloud Run

**Issue: Slow response times**

-   Increase Cloud Run memory allocation
-   Consider setting minimum instances > 0
-   Optimize model selection for sub-agents
