"""
Service interfaces for Terminal AI Companion
"""

from .imemory_service import IMemoryService
from .iai_conversation_service import IAIConversationService
from .ipersonality_service import IPersonalityService
from .iui_service import IUIService

__all__ = [
    'IMemoryService',
    'IAIConversationService',
    'IPersonalityService',
    'IUIService'
]