# Terminal AI Companion 💝

> Enterprise-grade terminal-based AI companion with memory, personality, and emotional intelligence

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Cross Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com)

## 🚀 Quick Start

### One-Click Setup & Run

**Windows:**

```batch
run.bat
```

**macOS/Linux:**

```bash
./run.sh
```

That's it! The script will automatically:

- Check Python installation
- Create virtual environment
- Install dependencies
- Set up configuration
- Launch the application

### Manual Setup

```bash
# 1. Clone and navigate
git clone <repository-url>
cd terminal-companion

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key

# 6. Run
python main.py
```

## ✨ Features

### 🧠 Memory System

- **Long-term Memory**: Persistent storage using self-hosted mem0
- **Short-term Memory**: Session-based conversation context
- **Smart Retrieval**: Vector-based memory search
- **User Preferences**: Learns and remembers your likes/dislikes

### 🎭 Personality Types

- **돌봄이 (Caring)**: Warm and nurturing personality
- **장난꾸러기 (Playful)**: Fun and humorous interactions
- **현자 (Intellectual)**: Deep and thoughtful conversations
- **로맨틱 (Romantic)**: Affectionate and loving expressions

### 🎯 Emotional Intelligence

- **Sentiment Analysis**: Understands your emotional state
- **Context Awareness**: Adapts responses to conversation context
- **Mood Tracking**: Monitors and responds to your feelings
- **Empathetic Responses**: Provides appropriate emotional support

### 🔧 Enterprise Architecture

- **Modular Design**: Clean separation of concerns
- **Interface-Based**: Easily extensible and testable
- **Configuration Management**: Environment-based settings
- **Comprehensive Logging**: Detailed operation tracking
- **Error Resilience**: Graceful degradation on failures

## 📋 Commands

| Command                | Description               |
| ---------------------- | ------------------------- |
| `help`, `도움말`       | Show help information     |
| `personality`, `성격`  | Change personality type   |
| `stats`, `통계`        | Display system statistics |
| `clear`, `클리어`      | Clear screen              |
| `memory`, `기억`       | Memory management menu    |
| `config`, `설정`       | Show configuration info   |
| `quit`, `exit`, `종료` | Exit application          |

## ⚙️ Configuration

Edit `.env` file to customize your companion:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Companion Settings
COMPANION_NAME=AI동반자
COMPANION_DEFAULT_PERSONALITY=caring

# UI Preferences
UI_THEME=magenta
UI_SHOW_TYPING_ANIMATION=true

# Memory Settings
MEMORY_SEARCH_LIMIT=5
MAX_SESSION_MEMORIES=100
```

## 🏗️ Architecture

```
src/
├── Config/         # Configuration management
├── Controller/     # Application orchestration
├── Entity/         # Data models and DTOs
├── IService/       # Service interfaces
├── Service/        # Business logic implementation
├── UI/             # User interface components
└── Utils/          # Shared utilities
```

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## 🔧 Development

### Project Structure

```
├── src/            # Source code with layered architecture
├── logs/           # Application logs
├── docs/           # Project documentation
├── main.py         # Application entry point
├── run.bat         # Windows runner
├── run.sh          # Unix runner
└── .env.example    # Configuration template
```

### Key Components

- **CompanionController**: Main application orchestrator
- **MemoryService**: Handles short/long-term memory with mem0
- **PersonalityService**: Manages 4 distinct personality types
- **AIConversationService**: OpenAI integration with fallback
- **TerminalUIService**: Rich cross-platform terminal interface

### Adding New Features

1. **New Personality**: Extend `PERSONALITY_TRAITS` in `PersonalityService`
2. **New Commands**: Add to `process_command()` in `CompanionController`
3. **New Memory Types**: Extend `MemoryType` enum and update services
4. **New UI Elements**: Extend `TerminalUIService` methods

## 📦 Dependencies

### Core Dependencies

- `mem0ai` - Memory management with vector storage
- `openai` - OpenAI API client for conversations
- `rich` - Beautiful terminal UI components
- `colorama` - Cross-platform colored terminal text
- `python-dotenv` - Environment variable management

### System Requirements

- Python 3.8+
- 50MB+ free disk space
- Internet connection (for OpenAI API)
- UTF-8 compatible terminal

## 🔒 Privacy & Security

- **Local Storage**: All conversations stored locally
- **No Data Transmission**: Conversations never leave your device
- **API Security**: Secure OpenAI API key handling
- **Open Source**: Transparent, auditable codebase

## 📊 Performance

- **Fast Startup**: < 2 seconds typical launch time
- **Memory Efficient**: < 100MB RAM usage
- **Responsive UI**: Real-time typing animations
- **Smart Caching**: Reduces API calls and improves speed

## 🐛 Troubleshooting

### Common Issues

**OpenAI API Error**

```bash
# Check your API key in .env file
echo $OPENAI_API_KEY  # Unix
set OPENAI_API_KEY    # Windows
```

**Memory System Fails**

- Application continues with session-only memory
- Check logs/ directory for detailed error information

**Installation Problems**

```bash
# Upgrade pip and try again
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Terminal Display Issues**

- Ensure your terminal supports UTF-8 encoding
- Try a modern terminal like Windows Terminal or iTerm2

### Logs

Check `logs/` directory for detailed error information:

```bash
# View latest log
cat logs/companion_$(date +%Y%m%d).log
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the existing architecture patterns
4. Add tests for new functionality
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open Pull Request

### Development Guidelines

- Follow existing code style and patterns
- Add type hints for all functions
- Include docstrings for public methods
- Write unit tests for business logic
- Update documentation for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [mem0](https://github.com/mem0ai/mem0) - Excellent memory management framework
- [OpenAI](https://openai.com/) - Powerful language model API
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal UI library
- Korean AI community for inspiration and feedback

---

💝 **Start meaningful conversations with your AI companion today!**

_Built with ❤️ for developers who value quality architecture and user experience._
