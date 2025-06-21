"""
애플리케이션 설정 관리
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

@dataclass
class AIProviderConfig:
    """AI 제공자 설정"""
    provider: str = "ollama"  # openai, openrouter, ollama
    
    # OpenAI 설정
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    
    # OpenRouter 설정
    openrouter_api_key: str = ""
    openrouter_model: str = "openai/gpt-4o-mini"
    
    # Ollama 설정
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma3:1b"
    
    # 공통 설정
    temperature: float = 0.7
    max_tokens: int = 500
    
    @classmethod
    def from_env(cls) -> 'AIProviderConfig':
        """환경 변수에서 설정 로드"""
        provider = os.getenv('AI_PROVIDER', 'ollama')
        
        openai_api_key = os.getenv('OPENAI_API_KEY', '')
        openai_model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        
        openrouter_api_key = os.getenv('OPENROUTER_API_KEY', '')
        openrouter_model = os.getenv('OPENROUTER_MODEL', 'openai/gpt-4o-mini')
        
        ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        ollama_model = os.getenv('OLLAMA_MODEL', 'gemma3:1b')
        
        temperature = float(os.getenv('AI_TEMPERATURE', '0.7'))
        max_tokens = int(os.getenv('AI_MAX_TOKENS', '500'))
        
        return cls(
            provider=provider,
            openai_api_key=openai_api_key,
            openai_model=openai_model,
            openrouter_api_key=openrouter_api_key,
            openrouter_model=openrouter_model,
            ollama_base_url=ollama_base_url,
            ollama_model=ollama_model,
            temperature=temperature,
            max_tokens=max_tokens
        )

@dataclass
class CompanionConfig:
    """동반자 설정"""
    name: str = "AI동반자"
    default_personality: str = "caring"
    user_id: str = "default_user"
    
    @classmethod
    def from_env(cls) -> 'CompanionConfig':
        """환경 변수에서 설정 로드"""
        name = os.getenv('COMPANION_NAME', 'AI동반자')
        personality = os.getenv('COMPANION_DEFAULT_PERSONALITY', 'caring')
        user_id = os.getenv('COMPANION_USER_ID', 'default_user')
        
        return cls(
            name=name,
            default_personality=personality,
            user_id=user_id
        )

@dataclass
class MemoryConfig:
    """메모리 시스템 설정"""
    provider: str = "mem0"
    vector_store: str = "chroma"
    max_session_memories: int = 100
    search_limit: int = 5
    
    # LLM 설정
    llm_provider: str = "ollama"
    llm_model: str = "gemma3:1b"
    llm_base_url: str = "http://localhost:11434"
    
    # 임베딩 설정
    embed_provider: str = "ollama"
    embed_model: str = "bge-m3"
    embed_base_url: str = "http://localhost:11434"
    
    @classmethod
    def from_env(cls) -> 'MemoryConfig':
        """환경 변수에서 설정 로드"""
        provider = os.getenv('MEMORY_PROVIDER', 'mem0')
        vector_store = os.getenv('MEMORY_VECTOR_STORE', 'chroma')
        max_session = int(os.getenv('MAX_SESSION_MEMORIES', '100'))
        search_limit = int(os.getenv('MEMORY_SEARCH_LIMIT', '5'))
        
        # LLM 설정
        llm_provider = os.getenv('MEMORY_LLM_PROVIDER', 'ollama')
        llm_model = os.getenv('MEMORY_LLM_MODEL', 'gemma3:1b')
        llm_base_url = os.getenv('MEMORY_LLM_BASE_URL', 'http://localhost:11434')
        
        # 임베딩 설정
        embed_provider = os.getenv('MEMORY_EMBED_PROVIDER', 'ollama')
        embed_model = os.getenv('MEMORY_EMBED_MODEL', 'bge-m3')
        embed_base_url = os.getenv('MEMORY_EMBED_BASE_URL', 'http://localhost:11434')
        
        return cls(
            provider=provider,
            vector_store=vector_store,
            max_session_memories=max_session,
            search_limit=search_limit,
            llm_provider=llm_provider,
            llm_model=llm_model,
            llm_base_url=llm_base_url,
            embed_provider=embed_provider,
            embed_model=embed_model,
            embed_base_url=embed_base_url
        )

@dataclass
class UIConfig:
    """UI 설정"""
    theme: str = "magenta"
    show_typing_animation: bool = True
    animation_duration: float = 1.0
    clear_screen_on_start: bool = True
    
    @classmethod
    def from_env(cls) -> 'UIConfig':
        """환경 변수에서 설정 로드"""
        theme = os.getenv('UI_THEME', 'magenta')
        show_animation = os.getenv('UI_SHOW_TYPING_ANIMATION', 'true').lower() == 'true'
        animation_duration = float(os.getenv('UI_ANIMATION_DURATION', '1.0'))
        clear_screen = os.getenv('UI_CLEAR_SCREEN_ON_START', 'true').lower() == 'true'
        
        return cls(
            theme=theme,
            show_typing_animation=show_animation,
            animation_duration=animation_duration,
            clear_screen_on_start=clear_screen
        )

@dataclass
class LoggingConfig:
    """로깅 설정"""
    level: str = "INFO"
    log_dir: str = "logs"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def from_env(cls) -> 'LoggingConfig':
        """환경 변수에서 설정 로드"""
        level = os.getenv('LOG_LEVEL', 'INFO')
        log_dir = os.getenv('LOG_DIR', 'logs')
        max_size = int(os.getenv('LOG_MAX_FILE_SIZE', str(10 * 1024 * 1024)))
        backup_count = int(os.getenv('LOG_BACKUP_COUNT', '5'))
        log_format = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        return cls(
            level=level,
            log_dir=log_dir,
            max_file_size=max_size,
            backup_count=backup_count,
            format=log_format
        )

class AppConfig:
    """전체 애플리케이션 설정 관리"""
    
    def __init__(self):
        self.ai = AIProviderConfig.from_env()
        self.companion = CompanionConfig.from_env()
        self.memory = MemoryConfig.from_env()
        self.ui = UIConfig.from_env()
        self.logging = LoggingConfig.from_env()
        
        # 로그 디렉토리 생성
        os.makedirs(self.logging.log_dir, exist_ok=True)
    
    def validate(self) -> Dict[str, bool]:
        """설정 유효성 검사"""
        validation_results = {}
        
        # AI 제공자별 API 키 검사
        if self.ai.provider == 'openai':
            validation_results['api_key'] = bool(self.ai.openai_api_key)
        elif self.ai.provider == 'openrouter':
            validation_results['api_key'] = bool(self.ai.openrouter_api_key)
        elif self.ai.provider == 'ollama':
            validation_results['api_key'] = True  # Ollama는 API 키 불필요
        
        # 성격 타입 검사
        valid_personalities = ['caring', 'playful', 'intellectual', 'romantic']
        validation_results['personality'] = self.companion.default_personality in valid_personalities
        
        # AI 제공자 검사
        valid_providers = ['openai', 'openrouter', 'ollama']
        validation_results['ai_provider'] = self.ai.provider in valid_providers
        
        # 로그 디렉토리 검사
        validation_results['log_directory'] = os.path.exists(self.logging.log_dir)
        
        return validation_results
    
    def get_validation_summary(self) -> str:
        """설정 검증 요약 반환"""
        results = self.validate()
        summary = []
        
        for key, valid in results.items():
            status = "✅" if valid else "❌"
            summary.append(f"{status} {key}")
        
        return "\n".join(summary)
    
    def to_dict(self) -> Dict[str, Any]:
        """설정을 딕셔너리로 변환"""
        return {
            'ai': {
                'provider': self.ai.provider,
                'temperature': self.ai.temperature,
                'max_tokens': self.ai.max_tokens,
                'openai_api_key_set': bool(self.ai.openai_api_key),
                'openrouter_api_key_set': bool(self.ai.openrouter_api_key),
                'models': {
                    'openai': self.ai.openai_model,
                    'openrouter': self.ai.openrouter_model,
                    'ollama': self.ai.ollama_model
                }
            },
            'companion': {
                'name': self.companion.name,
                'default_personality': self.companion.default_personality,
                'user_id': self.companion.user_id
            },
            'memory': {
                'provider': self.memory.provider,
                'vector_store': self.memory.vector_store,
                'max_session_memories': self.memory.max_session_memories,
                'search_limit': self.memory.search_limit
            },
            'ui': {
                'theme': self.ui.theme,
                'show_typing_animation': self.ui.show_typing_animation,
                'animation_duration': self.ui.animation_duration,
                'clear_screen_on_start': self.ui.clear_screen_on_start
            },
            'logging': {
                'level': self.logging.level,
                'log_dir': self.logging.log_dir,
                'max_file_size': self.logging.max_file_size,
                'backup_count': self.logging.backup_count
            }
        }

# 전역 설정 인스턴스
config = AppConfig()