"""
메모리 서비스 인터페이스
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from ..Entity import MemoryEntry, MemorySearchResult, MemoryStats, ConversationEntry

class IMemoryService(ABC):
    """메모리 서비스 인터페이스"""
    
    @abstractmethod
    def initialize(self, openai_client=None) -> bool:
        """메모리 시스템 초기화"""
        pass
    
    @abstractmethod
    def add_conversation(
        self,
        user_message: str,
        assistant_response: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """대화 내용을 메모리에 추가"""
        pass
    
    @abstractmethod
    def search_memories(self, query: str, limit: int = 5) -> MemorySearchResult:
        """관련 기억 검색"""
        pass
    
    @abstractmethod
    def add_user_preference(self, preference_type: str, preference_value: Any) -> bool:
        """사용자 선호도 저장"""
        pass
    
    @abstractmethod
    def get_user_preferences(self) -> List[MemoryEntry]:
        """사용자 선호도 검색"""
        pass
    
    @abstractmethod
    def get_conversation_history(self, limit: int = 10) -> List[ConversationEntry]:
        """최근 대화 이력 반환"""
        pass
    
    @abstractmethod
    def clear_session_memory(self) -> bool:
        """세션 메모리 초기화"""
        pass
    
    @abstractmethod
    def get_memory_stats(self) -> MemoryStats:
        """메모리 사용 통계"""
        pass