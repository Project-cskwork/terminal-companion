# Terminal AI Companion - Architecture Documentation

## 📁 Project Structure

```
terminal-companion/
├── src/                        # Source code
│   ├── Config/                 # Configuration management
│   │   ├── __init__.py
│   │   └── app_config.py       # Application configuration classes
│   ├── Controller/             # Application controllers
│   │   ├── __init__.py
│   │   └── companion_controller.py  # Main application controller
│   ├── Entity/                 # Data entities and DTOs
│   │   ├── __init__.py
│   │   ├── conversation.py     # Conversation related entities
│   │   ├── memory.py          # Memory entities
│   │   └── user_profile.py    # User profile entities
│   ├── IService/               # Service interfaces
│   │   ├── __init__.py
│   │   ├── iai_conversation_service.py
│   │   ├── imemory_service.py
│   │   ├── ipersonality_service.py
│   │   └── iui_service.py
│   ├── Service/                # Service implementations
│   │   ├── __init__.py
│   │   ├── ai_conversation_service.py
│   │   ├── memory_service.py
│   │   └── personality_service.py
│   ├── UI/                     # User interface
│   │   ├── __init__.py
│   │   └── terminal_ui.py      # Terminal UI implementation
│   ├── Utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── file_manager.py     # File operations
│   │   └── logger.py          # Logging utilities
│   └── __init__.py
├── logs/                       # Log files
├── docs/                       # Documentation
│   └── ARCHITECTURE.md         # This file
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows one-click runner
├── run.sh                      # Unix one-click runner
├── .env.example               # Environment configuration template
├── .gitignore                 # Git ignore rules
└── README.md                  # User documentation
```

## 🏗️ Architecture Overview

### Layered Architecture

The application follows a clean layered architecture pattern:

1. **Controller Layer** - Orchestrates business logic and user interactions
2. **Service Layer** - Contains business logic and external integrations
3. **Entity Layer** - Data models and domain objects
4. **UI Layer** - User interface components
5. **Utils Layer** - Shared utilities and helpers
6. **Config Layer** - Configuration management

### Design Patterns

- **Dependency Injection** - Services are injected into controllers
- **Repository Pattern** - Data access abstraction through services
- **Factory Pattern** - Entity creation from dictionaries
- **Strategy Pattern** - Multiple personality types with different behaviors
- **Observer Pattern** - Event-driven updates between components

## 📋 Component Details

### Configuration (`src/Config/`)

Manages all application configuration using environment variables and dataclasses:

- **AppConfig** - Main configuration container
- **OpenAIConfig** - OpenAI API settings
- **CompanionConfig** - Companion behavior settings
- **MemoryConfig** - Memory system configuration
- **UIConfig** - User interface preferences
- **LoggingConfig** - Logging system setup

### Entities (`src/Entity/`)

Domain models representing core business objects:

#### Conversation Entities
- **Message** - Individual chat message
- **ConversationEntry** - User-assistant conversation pair
- **ConversationHistory** - Collection of conversation entries

#### User Profile Entities
- **UserProfile** - Complete user information
- **UserPreference** - Individual user preferences
- **UserStats** - Usage statistics

#### Memory Entities
- **MemoryEntry** - Individual memory item
- **MemorySearchResult** - Search operation results
- **MemoryStats** - Memory system statistics

### Services (`src/Service/`)

Business logic implementations:

#### AIConversationService
- OpenAI API integration
- Response generation
- Sentiment analysis
- Preference extraction

#### MemoryService
- Long-term memory (mem0 integration)
- Short-term session memory
- Memory search and retrieval
- User preference storage

#### PersonalityService
- Multiple personality types (Caring, Playful, Intellectual, Romantic)
- Context-aware response generation
- Mood and interaction tracking
- System prompt generation

### User Interface (`src/UI/`)

#### TerminalUIService
- Cross-platform terminal interface
- Rich text formatting and colors
- Interactive menus and prompts
- Progress indicators and animations

### Utilities (`src/Utils/`)

#### FileManager
- Safe file operations
- JSON serialization
- Backup management
- File cleanup utilities

#### Logger
- Structured logging setup
- Log rotation and cleanup
- Module-specific loggers
- Configurable log levels

### Controller (`src/Controller/`)

#### CompanionController
- Main application orchestration
- User session management
- Command processing
- Service coordination

## 🔄 Data Flow

1. **User Input** → Controller receives input via UI Service
2. **Command Processing** → Controller determines if input is command or conversation
3. **Service Orchestration** → Controller coordinates between services:
   - Memory Service searches for relevant memories
   - Personality Service generates system prompt
   - AI Service generates response
4. **Response Processing** → Controller processes AI response and updates:
   - Memory Service stores conversation
   - Personality Service updates interaction state
   - User Profile updates preferences and stats
5. **Output** → Controller displays response via UI Service

## 🔧 Configuration Management

The application uses a hierarchical configuration system:

1. **Default Values** - Hardcoded in dataclasses
2. **Environment Variables** - Loaded from `.env` file
3. **Runtime Configuration** - Can be modified during execution

Configuration validation ensures all required settings are properly configured.

## 📊 Memory Architecture

### Two-Tier Memory System

1. **Session Memory** - Fast, in-memory storage for current session
2. **Long-term Memory** - Persistent storage using mem0 with vector search

### Memory Types
- **Conversation** - User-assistant dialogues
- **Preference** - User likes/dislikes
- **Fact** - Factual information about user
- **Emotion** - Emotional context and reactions

## 🎭 Personality System

### Personality Types

Each personality has distinct characteristics:

- **Response Style** - How the AI communicates
- **Greeting Phrases** - Personality-specific greetings
- **Contextual Responses** - Situation-appropriate reactions
- **Mood Management** - Emotional state tracking

### Dynamic Adaptation

- **Sentiment Analysis** - Adjusts to user's emotional state
- **Interaction Learning** - Improves responses over time
- **Preference Integration** - Incorporates user preferences

## 🔍 Error Handling

### Graceful Degradation

- **API Failures** - Falls back to rule-based responses
- **Memory Issues** - Uses session memory only
- **Configuration Problems** - Uses default values

### Logging Strategy

- **Debug** - Detailed operation traces
- **Info** - Important state changes
- **Warning** - Recoverable issues
- **Error** - Serious problems requiring attention

## 🚀 Performance Considerations

### Memory Management
- **Session Limits** - Prevents memory bloat
- **Lazy Loading** - Services initialized on demand
- **Efficient Search** - Vector-based memory retrieval

### Responsiveness
- **Async Operations** - Non-blocking UI updates
- **Caching** - Reduces repeated API calls
- **Batch Processing** - Efficient bulk operations

## 🔒 Security

### Data Protection
- **Local Storage** - All data stored locally
- **API Key Security** - Secure environment variable handling
- **Input Validation** - Prevents injection attacks

### Privacy
- **No Data Transmission** - Conversations stay on device
- **User Control** - Users own their data
- **Transparent Operations** - Open source codebase

## 🧪 Testing Strategy

### Unit Testing
- **Service Layer** - Business logic validation
- **Entity Classes** - Data model correctness
- **Utility Functions** - Helper function reliability

### Integration Testing
- **Service Interactions** - Cross-service communication
- **External APIs** - Third-party integration
- **File Operations** - Data persistence

### End-to-End Testing
- **User Workflows** - Complete user journeys
- **Error Scenarios** - Failure handling
- **Performance** - System responsiveness

## 📈 Extensibility

### Adding New Services
1. Create interface in `IService/`
2. Implement in `Service/`
3. Register in `Controller/`

### Adding New Personalities
1. Extend `PERSONALITY_TRAITS` in `PersonalityService`
2. Add new `PersonalityType` enum value
3. Update UI personality menu

### Adding New Memory Types
1. Add to `MemoryType` enum
2. Update memory service handling
3. Modify search and retrieval logic

## 🔧 Maintenance

### Log Management
- **Automatic Rotation** - Prevents disk space issues
- **Configurable Retention** - Adjustable log history
- **Performance Monitoring** - Track system health

### Data Migration
- **Version Compatibility** - Backward compatible data formats
- **Schema Evolution** - Graceful data structure changes
- **Backup Strategy** - Automatic data protection

This architecture provides a solid foundation for a maintainable, extensible, and robust AI companion application.