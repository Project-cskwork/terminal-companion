"""
Entity definitions for Terminal AI Companion
"""

from .conversation import (
    Message,
    MessageRole,
    SentimentType,
    ConversationEntry,
    ConversationHistory
)
from .user_profile import (
    PersonalityType,
    UserPreference,
    UserStats,
    UserProfile
)
from .memory import (
    MemoryType,
    MemoryEntry,
    MemorySearchResult,
    MemoryStats
)

__all__ = [
    # Conversation entities
    'Message',
    'MessageRole',
    'SentimentType',
    'ConversationEntry',
    'ConversationHistory',
    
    # User profile entities
    'PersonalityType',
    'UserPreference',
    'UserStats',
    'UserProfile',
    
    # Memory entities
    'MemoryType',
    'MemoryEntry',
    'MemorySearchResult',
    'MemoryStats'
]