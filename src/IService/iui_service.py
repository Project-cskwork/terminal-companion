"""
UI 서비스 인터페이스
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class IUIService(ABC):
    """UI 서비스 인터페이스"""
    
    @abstractmethod
    def clear_screen(self) -> None:
        """화면 클리어"""
        pass
    
    @abstractmethod
    def display_welcome(self, companion_name: str, personality_type: str) -> None:
        """환영 화면 표시"""
        pass
    
    @abstractmethod
    def display_help(self) -> None:
        """도움말 표시"""
        pass
    
    @abstractmethod
    def get_user_input(self, user_name: str = "당신") -> str:
        """사용자 입력 받기"""
        pass
    
    @abstractmethod
    def display_message(self, message: str, sender: str = "AI", style: Optional[str] = None) -> None:
        """메시지 표시"""
        pass
    
    @abstractmethod
    def display_typing_animation(self, duration: float = 2.0) -> None:
        """타이핑 애니메이션 표시"""
        pass
    
    @abstractmethod
    def display_error(self, error_message: str) -> None:
        """에러 메시지 표시"""
        pass
    
    @abstractmethod
    def display_success(self, success_message: str) -> None:
        """성공 메시지 표시"""
        pass
    
    @abstractmethod
    def display_warning(self, warning_message: str) -> None:
        """경고 메시지 표시"""
        pass
    
    @abstractmethod
    def display_info(self, info_message: str) -> None:
        """정보 메시지 표시"""
        pass
    
    @abstractmethod
    def display_personality_menu(
        self, 
        personalities: List[Dict], 
        current_personality: str
    ) -> Optional[str]:
        """성격 선택 메뉴 표시"""
        pass
    
    @abstractmethod
    def display_stats(self, memory_stats: Dict, personality_stats: Dict) -> None:
        """시스템 통계 표시"""
        pass
    
    @abstractmethod
    def confirm_action(self, message: str) -> bool:
        """사용자 확인 받기"""
        pass
    
    @abstractmethod
    def display_goodbye(self, user_name: str = "") -> None:
        """작별 인사 표시"""
        pass