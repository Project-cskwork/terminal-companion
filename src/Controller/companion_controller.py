"""
동반자 컨트롤러 - 메인 애플리케이션 로직 관리
"""

import logging
from datetime import datetime
from typing import Dict, Optional

from ..Config import config
from ..Entity import UserProfile, PersonalityType, SentimentType, ConversationEntry
from ..Service import MemoryService, AIConversationService, PersonalityService
from ..UI import TerminalUIService
from ..Utils import FileManager, get_logger

logger = get_logger(__name__)

class CompanionController:
    """동반자 애플리케이션 컨트롤러"""
    
    def __init__(self):
        # 기본 설정
        self.user_id = config.companion.user_id
        self.companion_name = config.companion.name
        self.session_start = datetime.now()
        self.is_running = True
        
        # 사용자 프로필 로드
        self.user_profile = self._load_user_profile()
        
        # 서비스 초기화
        self.memory_service = MemoryService(self.user_id)
        self.ai_service = AIConversationService()
        self.personality_service = PersonalityService(
            PersonalityType(self.user_profile.preferred_personality)
        )
        self.ui_service = TerminalUIService()
        
        logger.info("CompanionController가 초기화되었습니다.")
    
    def _load_user_profile(self) -> UserProfile:
        """사용자 프로필 로드"""
        profile_data = FileManager.load_json("user_profile.json")
        
        if profile_data and "user_id" in profile_data:
            try:
                profile = UserProfile.from_dict(profile_data)
                logger.info(f"사용자 프로필 로드됨: {profile.name}")
                return profile
            except Exception as e:
                logger.error(f"프로필 파싱 실패: {e}")
        
        # 새 프로필 생성
        logger.info("새 사용자 프로필 생성")
        return UserProfile(
            user_id=self.user_id,
            preferred_personality=PersonalityType(config.companion.default_personality)
        )
    
    def _save_user_profile(self) -> bool:
        """사용자 프로필 저장"""
        try:
            self.user_profile.updated_at = datetime.now()
            profile_data = self.user_profile.to_dict()
            
            success = FileManager.save_json(profile_data, "user_profile.json")
            if success:
                logger.debug("사용자 프로필 저장 완료")
            else:
                logger.error("사용자 프로필 저장 실패")
            
            return success
            
        except Exception as e:
            logger.error(f"프로필 저장 중 오류: {e}")
            self.ui_service.display_error(f"프로필 저장 실패: {e}")
            return False
    
    def initialize_systems(self) -> bool:
        """모든 시스템 초기화"""
        success_count = 0
        
        # AI 대화 시스템 초기화
        if self.ai_service.initialize():
            self.ui_service.display_success("AI 대화 시스템 초기화 완료")
            success_count += 1
        else:
            self.ui_service.display_warning("AI 대화 시스템이 기본 모드로 실행됩니다")
        
        # 메모리 시스템 초기화
        if self.memory_service.initialize(self.ai_service.openai_client):
            self.ui_service.display_success("메모리 시스템 초기화 완료")
            success_count += 1
        else:
            self.ui_service.display_warning("메모리 시스템이 세션 모드로 실행됩니다")
        
        logger.info(f"시스템 초기화 완료: {success_count}/2 성공")
        return success_count > 0
    
    def setup_user_profile(self):
        """사용자 프로필 설정"""
        if not self.user_profile.name:
            name = self.ui_service.get_user_input("처음 뵙겠습니다! 이름을 알려주세요")
            if name and name.lower() not in ['quit', 'exit', '종료', '나가기']:
                self.user_profile.name = name
                self._save_user_profile()
                self.ui_service.display_success(f"반가워요, {name}님! 🌟")
        else:
            self.ui_service.display_info(f"다시 만나서 반가워요, {self.user_profile.name}님!")
    
    def process_command(self, user_input: str) -> Optional[bool]:
        """특수 명령어 처리"""
        command = user_input.lower().strip()
        
        if command in ['quit', 'exit', '종료', '나가기']:
            return False
        
        elif command in ['help', '도움말']:
            self.ui_service.display_help()
            return True
        
        elif command in ['personality', '성격']:
            self._handle_personality_change()
            return True
        
        elif command in ['stats', '통계']:
            self._display_system_stats()
            return True
        
        elif command in ['clear', '클리어']:
            self.ui_service.clear_screen()
            return True
        
        elif command in ['memory', '기억']:
            self._handle_memory_menu()
            return True
        
        elif command in ['config', '설정']:
            self._display_config_info()
            return True
        
        elif command in ['provider', 'ai']:
            self._handle_provider_change()
            return True
        
        elif command in ['model', '모델']:
            self._handle_model_change()
            return True
        
        return None  # 일반 대화로 처리
    
    def _handle_personality_change(self):
        """성격 변경 처리"""
        personalities = self.personality_service.get_available_personalities()
        current = self.personality_service.personality_type.value
        
        selected = self.ui_service.display_personality_menu(personalities, current)
        if selected and selected != current:
            new_personality = PersonalityType(selected)
            if self.personality_service.change_personality(new_personality):
                self.ui_service.display_success(
                    f"성격이 '{self.personality_service.get_personality_info()['name']}'로 변경되었습니다!"
                )
                self.user_profile.preferred_personality = new_personality
                self._save_user_profile()
            else:
                self.ui_service.display_error("성격 변경에 실패했습니다.")
    
    def _display_system_stats(self):
        """시스템 통계 표시"""
        memory_stats = self.memory_service.get_memory_stats().to_dict()
        personality_stats = self.personality_service.get_personality_stats()
        conversation_stats = self.ai_service.get_conversation_stats()
        
        # AI 통계 추가
        ai_stats = conversation_stats.copy()
        ai_stats.update({
            "current_provider": self.ai_service.get_current_provider(),
            "current_model": self.ai_service.get_current_model()
        })
        
        self.ui_service.display_stats(memory_stats, personality_stats)
        self.ui_service.display_ai_stats(ai_stats)
    
    def _handle_memory_menu(self):
        """메모리 관리 메뉴"""
        self.ui_service.display_info("메모리 관리 기능:")
        
        # 메모리 통계 표시
        stats = self.memory_service.get_memory_stats()
        self.ui_service.display_info(f"세션 메모리: {stats.session_memories}개")
        self.ui_service.display_info(f"장기 메모리: {'활성화' if stats.long_term_enabled else '비활성화'}")
        
        # 메모리 초기화 옵션
        if stats.session_memories > 0:
            if self.ui_service.confirm_action("세션 메모리를 초기화하시겠습니까?"):
                if self.memory_service.clear_session_memory():
                    self.ui_service.display_success("세션 메모리가 초기화되었습니다.")
    
    def _display_config_info(self):
        """설정 정보 표시"""
        self.ui_service.display_info("현재 설정:")
        self.ui_service.display_info(f"동반자 이름: {config.companion.name}")
        self.ui_service.display_info(f"기본 성격: {config.companion.default_personality}")
        self.ui_service.display_info(f"AI 제공자: {config.ai.provider}")
        self.ui_service.display_info(f"AI 모델: {self.ai_service.get_current_model()}")
        self.ui_service.display_info(f"UI 테마: {config.ui.theme}")
        
        # 설정 검증 결과
        validation_summary = config.get_validation_summary()
        self.ui_service.display_info(f"설정 검증:\n{validation_summary}")
    
    def _handle_provider_change(self):
        """AI 제공자 변경 처리"""
        providers = self.ai_service.get_available_providers()
        current = self.ai_service.get_current_provider()
        
        selected = self.ui_service.display_provider_menu(providers, current)
        if selected and selected != current:
            if self.ai_service.set_provider(selected):
                self.ui_service.display_success(f"AI 제공자가 '{selected.upper()}'로 변경되었습니다!")
                
                # 새 제공자로 재초기화
                if self.ai_service.initialize():
                    self.ui_service.display_success("새 AI 제공자로 성공적으로 연결되었습니다.")
                else:
                    self.ui_service.display_warning("새 AI 제공자 연결에 실패했습니다. 기본 모드로 실행됩니다.")
            else:
                self.ui_service.display_error("AI 제공자 변경에 실패했습니다.")
    
    def _handle_model_change(self):
        """AI 모델 변경 처리"""
        current_provider = self.ai_service.get_current_provider()
        models = self.ai_service.get_available_models()
        current_model = self.ai_service.get_current_model()
        
        if not models:
            self.ui_service.display_error("사용 가능한 모델이 없습니다.")
            return
        
        selected = self.ui_service.display_model_menu(models, current_model, current_provider)
        if selected and selected != current_model:
            if self.ai_service.set_model(selected):
                self.ui_service.display_success(f"AI 모델이 '{selected}'로 변경되었습니다!")
            else:
                self.ui_service.display_error("AI 모델 변경에 실패했습니다.")
    
    def generate_ai_response(self, user_message: str) -> str:
        """AI 응답 생성"""
        # 관련 기억 검색
        memory_result = self.memory_service.search_memories(user_message, limit=config.memory.search_limit)
        memory_texts = [entry.content for entry in memory_result.entries]
        
        # 대화 이력 가져오기
        conversation_history = self.memory_service.get_conversation_history(limit=5)
        
        # 시스템 프롬프트 생성
        user_preferences = {key: pref.value for key, pref in self.user_profile.preferences.items()}
        system_prompt = self.personality_service.generate_system_prompt(
            user_name=self.user_profile.name,
            memories=memory_texts,
            user_preferences=user_preferences
        )
        
        # AI 응답 생성
        response = self.ai_service.generate_response(
            user_message=user_message,
            system_prompt=system_prompt,
            conversation_history=conversation_history
        )
        
        return response or "죄송해요, 응답을 생성할 수 없었어요."
    
    def process_conversation(self, user_message: str):
        """대화 처리"""
        try:
            # 감정 분석
            sentiment = self.ai_service.analyze_sentiment(user_message)
            
            # 선호도 추출 및 저장
            preferences = self.ai_service.extract_preferences(user_message)
            if preferences:
                for pref_type, pref_value in preferences.items():
                    self.user_profile.add_preference(pref_type, pref_value)
                    self.memory_service.add_user_preference(pref_type, pref_value)
                
                self._save_user_profile()
                logger.debug(f"새로운 선호도 저장: {preferences}")
            
            # AI 응답 생성
            if config.ui.show_typing_animation:
                self.ui_service.display_typing_animation()
            
            response = self.generate_ai_response(user_message)
            
            # 응답 표시
            self.ui_service.display_message(response, self.companion_name)
            
            # 메모리에 대화 저장
            conversation_entry = ConversationEntry(
                user_message=user_message,
                assistant_response=response,
                sentiment=sentiment,
                metadata={"session_id": str(self.session_start)}
            )
            
            self.memory_service.add_conversation(
                user_message,
                response,
                conversation_entry.metadata
            )
            
            # 성격 시스템 및 사용자 통계 업데이트
            self.personality_service.update_interaction(user_message, sentiment)
            self.user_profile.update_stats(conversations_increment=1)
            
            logger.debug(f"대화 처리 완료: {user_message[:30]}...")
            
        except Exception as e:
            logger.error(f"대화 처리 중 오류: {e}")
            self.ui_service.display_error(f"대화 처리 중 오류가 발생했습니다: {e}")
    
    def run(self):
        """메인 실행 루프"""
        try:
            # 환영 화면 표시
            self.ui_service.display_welcome(
                self.companion_name,
                self.personality_service.get_personality_info()["name"]
            )
            
            # 시스템 초기화
            if not self.initialize_systems():
                self.ui_service.display_warning("일부 기능이 제한될 수 있습니다.")
            
            # 사용자 프로필 설정
            self.setup_user_profile()
            
            # 인사말 표시
            greeting = self.personality_service.get_greeting()
            self.ui_service.display_message(greeting, self.companion_name)
            
            self.ui_service.display_info("대화를 시작해보세요! (도움말: 'help' 입력)")
            
            # 메인 대화 루프
            while self.is_running:
                try:
                    user_input = self.ui_service.get_user_input(self.user_profile.name or '당신')
                    
                    if not user_input.strip():
                        continue
                    
                    # 명령어 처리
                    command_result = self.process_command(user_input)
                    if command_result is False:  # 종료 명령
                        break
                    elif command_result is True:  # 명령어 처리됨
                        continue
                    
                    # 일반 대화 처리
                    self.process_conversation(user_input)
                    
                except KeyboardInterrupt:
                    if self.ui_service.confirm_action("정말 종료하시겠습니까?"):
                        break
                    else:
                        continue
                        
                except Exception as e:
                    logger.error(f"메인 루프 오류: {e}")
                    self.ui_service.display_error(f"오류가 발생했습니다: {e}")
                    continue
            
            # 작별 인사
            self.ui_service.display_goodbye(self.user_profile.name)
            logger.info("애플리케이션 종료")
            
        except Exception as e:
            logger.error(f"치명적 오류: {e}")
            self.ui_service.display_error(f"시스템 오류: {e}")
        finally:
            # 정리 작업
            self._save_user_profile()
            
            # 세션 시간 업데이트
            session_duration = (datetime.now() - self.session_start).total_seconds()
            self.user_profile.update_stats(
                conversations_increment=0,
                session_time_increment=session_duration
            )
            self._save_user_profile()
            
            logger.info(f"세션 종료: {session_duration:.1f}초")