"""
Configuration module for Terminal AI Companion
"""

from .app_config import (
    AppConfig,
    AIProviderConfig,
    CompanionConfig,
    MemoryConfig,
    UIConfig,
    LoggingConfig,
    config
)

__all__ = [
    'AppConfig',
    'AIProviderConfig',
    'CompanionConfig',
    'MemoryConfig',
    'UIConfig',
    'LoggingConfig',
    'config'
]