"""
성격 시스템 서비스 인터페이스
"""

from abc import ABC, abstractmethod
from typing import Dict, List
from ..Entity import PersonalityType, SentimentType

class IPersonalityService(ABC):
    """성격 시스템 서비스 인터페이스"""
    
    @abstractmethod
    def get_personality_info(self) -> Dict[str, str]:
        """현재 성격 정보 반환"""
        pass
    
    @abstractmethod
    def get_response_style(self) -> str:
        """성격에 맞는 응답 스타일 반환"""
        pass
    
    @abstractmethod
    def get_greeting(self) -> str:
        """성격에 맞는 인사말 반환"""
        pass
    
    @abstractmethod
    def get_contextual_response_prefix(self, user_message: str) -> str:
        """문맥에 맞는 응답 접두사 생성"""
        pass
    
    @abstractmethod
    def generate_system_prompt(
        self,
        user_name: str = "",
        memories: List[str] = None,
        user_preferences: Dict = None
    ) -> str:
        """성격 기반 시스템 프롬프트 생성"""
        pass
    
    @abstractmethod
    def update_interaction(self, user_message: str, user_sentiment: SentimentType):
        """상호작용 후 성격 상태 업데이트"""
        pass
    
    @abstractmethod
    def change_personality(self, new_personality: PersonalityType) -> bool:
        """성격 변경"""
        pass
    
    @abstractmethod
    def get_available_personalities(self) -> List[Dict[str, str]]:
        """사용 가능한 성격 목록 반환"""
        pass
    
    @abstractmethod
    def get_personality_stats(self) -> Dict[str, any]:
        """성격 시스템 통계"""
        pass