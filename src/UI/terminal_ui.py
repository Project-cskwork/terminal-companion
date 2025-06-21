"""
터미널 UI 서비스 구현
"""

import os
import sys
import platform
import logging
from typing import Dict, List, Optional
from datetime import datetime
import colorama
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..IService import IUIService
from ..Config import config

# Windows 호환성을 위한 colorama 초기화
colorama.init()

logger = logging.getLogger(__name__)

class TerminalUIService(IUIService):
    """터미널 UI 서비스 구현 클래스"""
    
    def __init__(self):
        self.console = Console()
        self.platform = platform.system()
        self.is_windows = self.platform == "Windows"
        self.session_start = datetime.now()
        
        # 색상 테마 (설정에서 가져오기)
        self.colors = {
            "primary": config.ui.theme,
            "secondary": "cyan", 
            "success": "green",
            "warning": "yellow",
            "error": "red",
            "info": "blue",
            "user": "bold blue",
            "assistant": config.ui.theme
        }
    
    def clear_screen(self) -> None:
        """화면 클리어 (크로스 플랫폼)"""
        if config.ui.clear_screen_on_start:
            os.system('cls' if self.is_windows else 'clear')
    
    def get_terminal_size(self) -> tuple:
        """터미널 크기 반환"""
        try:
            return os.get_terminal_size()
        except OSError:
            return (80, 24)  # 기본값
    
    def display_welcome(self, companion_name: str, personality_type: str) -> None:
        """환영 화면 표시"""
        if config.ui.clear_screen_on_start:
            self.clear_screen()
        
        welcome_text = Text()
        welcome_text.append("💝 ", style="red")
        welcome_text.append("Terminal AI Companion", style=f"bold {self.colors['primary']}")
        welcome_text.append(" 💝", style="red")
        
        system_info = f"""
        🖥️  시스템: {self.platform} {platform.release()}
        ⏰ 시작 시간: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}
        🤖 동반자: {companion_name} ({personality_type} 성격)
        
        안녕하세요! 당신의 AI 동반자입니다. 
        당신과 함께 대화하고, 기억하고, 감정을 나누며 지적인 대화를 나눌 수 있어요.
        
        💡 도움말: 'help' 또는 '도움말' 입력
        🚪 종료: 'quit', 'exit', '종료', '나가기' 입력
        """
        
        panel = Panel(
            system_info,
            title=welcome_text,
            border_style=self.colors["primary"],
            padding=(1, 2)
        )
        self.console.print(panel)
        logger.info("환영 화면이 표시되었습니다.")
    
    def display_help(self) -> None:
        """도움말 표시"""
        help_table = Table(title="🌟 Terminal AI Companion 도움말", show_header=True, header_style="bold cyan")
        help_table.add_column("명령어", style="cyan", width=20)
        help_table.add_column("설명", style="white")
        
        commands = [
            ("help, 도움말", "이 도움말 표시"),
            ("quit, exit, 종료, 나가기", "프로그램 종료"),
            ("personality, 성격", "성격 변경 메뉴"),
            ("stats, 통계", "시스템 상태 및 통계 표시"),
            ("clear, 클리어", "화면 정리"),
            ("memory, 기억", "메모리 관리 메뉴"),
            ("provider, ai", "AI 제공자 변경 메뉴"),
            ("model, 모델", "AI 모델 변경 메뉴"),
        ]
        
        for cmd, desc in commands:
            help_table.add_row(cmd, desc)
        
        features_text = """
        💝 주요 기능:
        • 장기/단기 메모리로 당신을 기억해요
        • 4가지 성격 타입 (돌봄이, 장난꾸러기, 현자, 로맨틱)
        • 감정적이고 지적인 대화가 가능해요
        • 당신의 선호도를 학습하고 적응해요
        • 크로스 플랫폼 지원 (Windows/macOS/Linux)
        """
        
        self.console.print(help_table)
        self.console.print(Panel(features_text, title="기능 안내", border_style=self.colors["info"]))
        logger.debug("도움말이 표시되었습니다.")
    
    def get_user_input(self, user_name: str = "당신") -> str:
        """사용자 입력 받기"""
        try:
            user_input = Prompt.ask(f"\n[{self.colors['user']}]{user_name}[/{self.colors['user']}]")
            logger.debug(f"사용자 입력: {user_input[:50]}...")
            return user_input
        except KeyboardInterrupt:
            return "quit"
        except EOFError:
            return "quit"
    
    def display_message(self, message: str, sender: str = "AI", style: Optional[str] = None) -> None:
        """메시지 표시"""
        if not style:
            style = self.colors["assistant"] if sender == "AI" else self.colors["user"]
        
        panel = Panel(
            message,
            title=f"[bold {style}]{sender}[/bold {style}]",
            border_style=style,
            padding=(0, 1)
        )
        self.console.print(panel)
        logger.debug(f"{sender} 메시지 표시: {message[:50]}...")
    
    def display_typing_animation(self, duration: float = None) -> None:
        """타이핑 애니메이션 표시"""
        if not config.ui.show_typing_animation:
            return
        
        if duration is None:
            duration = config.ui.animation_duration
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task("AI가 생각하고 있어요...", total=None)
            import time
            time.sleep(duration)
    
    def display_error(self, error_message: str) -> None:
        """에러 메시지 표시"""
        self.console.print(f"[{self.colors['error']}]❌ 오류: {error_message}[/{self.colors['error']}]")
        logger.error(error_message)
    
    def display_success(self, success_message: str) -> None:
        """성공 메시지 표시"""
        self.console.print(f"[{self.colors['success']}]✅ {success_message}[/{self.colors['success']}]")
        logger.info(success_message)
    
    def display_warning(self, warning_message: str) -> None:
        """경고 메시지 표시"""
        self.console.print(f"[{self.colors['warning']}]⚠️  {warning_message}[/{self.colors['warning']}]")
        logger.warning(warning_message)
    
    def display_info(self, info_message: str) -> None:
        """정보 메시지 표시"""
        self.console.print(f"[{self.colors['info']}]ℹ️  {info_message}[/{self.colors['info']}]")
        logger.info(info_message)
    
    def display_personality_menu(
        self, 
        personalities: List[Dict], 
        current_personality: str
    ) -> Optional[str]:
        """성격 선택 메뉴 표시"""
        personality_table = Table(title="🎭 성격 선택", show_header=True, header_style="bold cyan")
        personality_table.add_column("번호", style="cyan", width=6)
        personality_table.add_column("성격", style=self.colors["primary"], width=15)
        personality_table.add_column("설명", style="white")
        personality_table.add_column("현재", style="green", width=8)
        
        for i, personality in enumerate(personalities, 1):
            current_mark = "✓" if personality["type"] == current_personality else ""
            personality_table.add_row(
                str(i),
                personality["name"],
                personality["description"],
                current_mark
            )
        
        self.console.print(personality_table)
        
        try:
            choice = Prompt.ask("성격을 선택하세요 (번호 입력, 0=취소)", choices=[str(i) for i in range(len(personalities) + 1)])
            if choice == "0":
                return None
            
            selected_index = int(choice) - 1
            if 0 <= selected_index < len(personalities):
                selected_type = personalities[selected_index]["type"]
                logger.info(f"성격 선택: {selected_type}")
                return selected_type
            
        except (ValueError, KeyboardInterrupt):
            pass
        
        return None
    
    def display_stats(self, memory_stats: Dict, personality_stats: Dict) -> None:
        """시스템 통계 표시"""
        # 메모리 통계
        memory_table = Table(title="💾 메모리 통계", show_header=False)
        memory_table.add_column("항목", style="cyan")
        memory_table.add_column("값", style="yellow")
        
        memory_table.add_row("세션 메모리", str(memory_stats.get("session_memories", 0)))
        memory_table.add_row("장기 메모리", "활성화" if memory_stats.get("long_term_enabled") else "비활성화")
        memory_table.add_row("사용자 ID", memory_stats.get("user_id", "unknown"))
        
        # 성격 통계
        personality_table = Table(title="🎭 성격 통계", show_header=False)
        personality_table.add_column("항목", style="cyan")
        personality_table.add_column("값", style="yellow")
        
        personality_table.add_row("현재 성격", personality_stats.get("personality_name", "알 수 없음"))
        personality_table.add_row("기분 수준", f"{personality_stats.get('mood_level', 0):.1f}/1.0")
        personality_table.add_row("상호작용 횟수", str(personality_stats.get("interaction_count", 0)))
        personality_table.add_row("대화 맥락", str(personality_stats.get("conversation_context_size", 0)))
        
        # 시스템 정보
        system_table = Table(title="🖥️  시스템 정보", show_header=False)
        system_table.add_column("항목", style="cyan")
        system_table.add_column("값", style="yellow")
        
        system_table.add_row("플랫폼", self.platform)
        system_table.add_row("터미널 크기", f"{self.get_terminal_size().columns}x{self.get_terminal_size().lines}")
        system_table.add_row("세션 시간", str(datetime.now() - self.session_start).split('.')[0])
        
        self.console.print(memory_table)
        self.console.print(personality_table)
        self.console.print(system_table)
        logger.debug("시스템 통계가 표시되었습니다.")
    
    def confirm_action(self, message: str) -> bool:
        """사용자 확인 받기"""
        try:
            result = Confirm.ask(message)
            logger.debug(f"확인 요청: {message} -> {result}")
            return result
        except KeyboardInterrupt:
            return False
    
    def display_goodbye(self, user_name: str = "") -> None:
        """작별 인사 표시"""
        goodbye_text = Text()
        goodbye_text.append("💝 ", style="red")
        goodbye_text.append("안녕히 가세요", style=f"bold {self.colors['primary']}")
        goodbye_text.append(" 💝", style="red")
        
        if user_name:
            message = f"안녕히 가세요, {user_name}님!\n다음에 또 만나요. 좋은 하루 되세요! 🌟"
        else:
            message = "안녕히 가세요!\n다음에 또 만나요. 좋은 하루 되세요! 🌟"
        
        panel = Panel(
            message,
            title=goodbye_text,
            border_style=self.colors["primary"],
            padding=(1, 2)
        )
        self.console.print(panel)
        logger.info("작별 인사가 표시되었습니다.")
    
    def display_provider_menu(
        self, 
        providers: List[str], 
        current_provider: str
    ) -> Optional[str]:
        """AI 제공자 선택 메뉴 표시"""
        provider_table = Table(title="🤖 AI 제공자 선택", show_header=True, header_style="bold cyan")
        provider_table.add_column("번호", style="cyan", width=6)
        provider_table.add_column("제공자", style=self.colors["primary"], width=15)
        provider_table.add_column("설명", style="white")
        provider_table.add_column("현재", style="green", width=8)
        
        provider_descriptions = {
            "openai": "OpenAI GPT 모델 (API 키 필요)",
            "openrouter": "다양한 AI 모델 선택 가능 (API 키 필요)",
            "ollama": "로컬 오픈소스 모델 (무료, 로컬 설치 필요)"
        }
        
        for i, provider in enumerate(providers, 1):
            current_mark = "✓" if provider == current_provider else ""
            description = provider_descriptions.get(provider, "알 수 없는 제공자")
            provider_table.add_row(
                str(i),
                provider.upper(),
                description,
                current_mark
            )
        
        self.console.print(provider_table)
        
        try:
            choice = Prompt.ask("AI 제공자를 선택하세요 (번호 입력, 0=취소)", choices=[str(i) for i in range(len(providers) + 1)])
            if choice == "0":
                return None
            
            selected_index = int(choice) - 1
            if 0 <= selected_index < len(providers):
                selected_provider = providers[selected_index]
                logger.info(f"AI 제공자 선택: {selected_provider}")
                return selected_provider
            
        except (ValueError, KeyboardInterrupt):
            pass
        
        return None
    
    def display_model_menu(
        self, 
        models: List[str], 
        current_model: str,
        provider: str
    ) -> Optional[str]:
        """AI 모델 선택 메뉴 표시"""
        model_table = Table(title=f"🧠 {provider.upper()} 모델 선택", show_header=True, header_style="bold cyan")
        model_table.add_column("번호", style="cyan", width=6)
        model_table.add_column("모델", style=self.colors["primary"], width=30)
        model_table.add_column("현재", style="green", width=8)
        
        for i, model in enumerate(models, 1):
            current_mark = "✓" if model == current_model else ""
            model_table.add_row(
                str(i),
                model,
                current_mark
            )
        
        self.console.print(model_table)
        
        try:
            choice = Prompt.ask("모델을 선택하세요 (번호 입력, 0=취소)", choices=[str(i) for i in range(len(models) + 1)])
            if choice == "0":
                return None
            
            selected_index = int(choice) - 1
            if 0 <= selected_index < len(models):
                selected_model = models[selected_index]
                logger.info(f"AI 모델 선택: {selected_model}")
                return selected_model
            
        except (ValueError, KeyboardInterrupt):
            pass
        
        return None
    
    def display_ai_stats(self, ai_stats: Dict) -> None:
        """AI 관련 통계 표시"""
        ai_table = Table(title="🤖 AI 통계", show_header=False)
        ai_table.add_column("항목", style="cyan")
        ai_table.add_column("값", style="yellow")
        
        ai_table.add_row("현재 제공자", ai_stats.get("current_provider", "알 수 없음"))
        ai_table.add_row("현재 모델", ai_stats.get("current_model", "알 수 없음"))
        ai_table.add_row("총 대화 수", str(ai_stats.get("total_conversations", 0)))
        ai_table.add_row("사용 토큰 수", str(ai_stats.get("total_tokens_used", 0)))
        
        last_conversation = ai_stats.get("last_conversation")
        if last_conversation:
            ai_table.add_row("마지막 대화", last_conversation[:19])  # 날짜 부분만
        
        self.console.print(ai_table)
        logger.debug("AI 통계가 표시되었습니다.")