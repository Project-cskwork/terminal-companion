# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Terminal AI Companion is an enterprise-grade terminal-based AI companion with memory, personality, and emotional intelligence. The application supports multiple AI providers (OpenAI, OpenRouter, Ollama) and features a modular, layered architecture with comprehensive memory management.

## Development Commands

### Running the Application
```bash
# One-click setup and run
./run.sh              # macOS/Linux
run.bat               # Windows

# Manual run
python main.py
```

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env file with your API keys and preferences
```

### Configuration
- Copy `.env.example` to `.env` and configure:
  - `AI_PROVIDER`: Choose between `openai`, `openrouter`, or `ollama`
  - API keys for chosen provider
  - Model settings and memory configuration
- The app defaults to using Ollama for local AI if no API keys are provided

## Architecture Overview

### Layered Architecture Pattern
- **Controller Layer** (`src/Controller/`): Application orchestration and user session management
- **Service Layer** (`src/Service/`): Business logic implementations
- **Entity Layer** (`src/Entity/`): Data models and domain objects  
- **Interface Layer** (`src/IService/`): Service contracts for dependency injection
- **UI Layer** (`src/UI/`): Terminal interface using Rich library
- **Utils Layer** (`src/Utils/`): Shared utilities (logging, file management)
- **Config Layer** (`src/Config/`): Environment-based configuration management

### Key Services
- **CompanionController**: Main application orchestrator managing user sessions and command processing
- **MemoryService**: Two-tier memory system (session + persistent mem0 with vector search)
- **PersonalityService**: 4 distinct personality types (Caring, Playful, Intellectual, Romantic)
- **AIConversationService**: Multi-provider AI integration (OpenAI, OpenRouter, Ollama)
- **TerminalUIService**: Cross-platform rich terminal interface

### Memory Architecture
- **Session Memory**: Fast in-memory storage for current conversation
- **Long-term Memory**: Persistent vector-based storage using mem0 framework
- **Memory Types**: Conversation, Preference, Fact, Emotion
- **Smart Retrieval**: Vector search with configurable limits

### Configuration System
Uses dataclass-based hierarchical configuration:
1. Default values in dataclasses
2. Environment variables from .env file  
3. Runtime modifications possible

Configuration is managed through `AppConfig` class with validation and separate configs for AI, Memory, UI, Logging, and Companion settings.

## Key Implementation Details

### Multi-Provider AI Support
The application abstracts AI providers through a unified interface, supporting:
- OpenAI GPT models
- OpenRouter for diverse model access
- Ollama for local AI models (default)

### Personality System
Each personality type has distinct response styles, greeting phrases, and contextual adaptations with sentiment analysis integration.

### Error Handling Strategy
- Graceful degradation (API failures fall back to rule-based responses)
- Comprehensive logging with rotation
- Session-only memory fallback if persistent memory fails

### File Structure Conventions
- Korean comments and documentation throughout codebase
- Factory pattern for entity creation from dictionaries
- Interface-based dependency injection
- Comprehensive logging with module-specific loggers

## Data Management

### User Profile
Stored in `user_profile.json` with automatic backup creation. Contains user preferences, statistics, and personality settings.

### Logging
- Automatic log rotation in `logs/` directory
- Configurable log levels and retention
- Daily log files with format: `companion_YYYYMMDD.log`

### Memory Storage
- Session data stored in memory
- Long-term memories persisted via mem0 framework
- Vector embeddings for semantic memory search

## Development Notes

- No test framework is currently implemented in the project
- The application uses Korean language extensively in comments and some user-facing text
- Cross-platform compatibility is built-in with separate Windows (.bat) and Unix (.sh) runners
- The codebase follows enterprise patterns with clean separation of concerns