"""
AI 대화 서비스 인터페이스
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from ..Entity import ConversationEntry, SentimentType

class IAIConversationService(ABC):
    """AI 대화 서비스 인터페이스"""
    
    @abstractmethod
    def initialize(self, api_key: Optional[str] = None) -> bool:
        """AI 대화 시스템 초기화"""
        pass
    
    @abstractmethod
    def generate_response(
        self,
        user_message: str,
        system_prompt: str,
        conversation_history: Optional[List[ConversationEntry]] = None,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[str]:
        """AI 응답 생성"""
        pass
    
    @abstractmethod
    def analyze_sentiment(self, text: str) -> SentimentType:
        """감정 분석"""
        pass
    
    @abstractmethod
    def extract_preferences(self, user_message: str) -> Dict[str, str]:
        """사용자 메시지에서 선호도 추출"""
        pass
    
    @abstractmethod
    def get_conversation_stats(self) -> Dict[str, any]:
        """대화 통계 반환"""
        pass
    
    @abstractmethod
    def set_model(self, model_name: str) -> bool:
        """사용할 모델 변경"""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """사용 가능한 모델 목록"""
        pass
    
    @abstractmethod
    def reset_stats(self) -> None:
        """통계 초기화"""
        pass