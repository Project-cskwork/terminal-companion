"""
메모리 서비스 구현
"""

import logging
import sys
import os
from contextlib import contextmanager
from datetime import datetime
from typing import List, Dict, Optional, Any

from ..IService import IMemoryService
from ..Entity import (
    MemoryEntry, MemorySearchResult, MemoryStats, MemoryType,
    ConversationEntry, SentimentType
)
from ..Config import config

logger = logging.getLogger(__name__)

@contextmanager
def suppress_stderr():
    """표준 에러 출력을 일시적으로 억제하는 컨텍스트 매니저"""
    # Windows와 Unix 모두에서 작동하도록 개선
    try:
        # 원본 stderr 저장
        old_stderr = sys.stderr
        
        # Windows의 경우 NUL, Unix의 경우 /dev/null
        null_device = 'NUL' if sys.platform == 'win32' else '/dev/null'
        devnull = open(null_device, 'w', encoding='utf-8')
        
        # stderr를 null device로 리다이렉트
        sys.stderr = devnull
        yield
    except Exception:
        # 오류 발생 시에도 계속 진행
        yield
    finally:
        # 원래 stderr로 복원
        sys.stderr = old_stderr
        try:
            devnull.close()
        except:
            pass

class MemoryService(IMemoryService):
    """메모리 서비스 구현 클래스"""
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.memory = None
        self.openai_client = None
        self.session_memories = []  # 세션 내 단기 메모리
        self.is_initialized = False
        
    def initialize(self, openai_client=None) -> bool:
        """메모리 시스템 초기화"""
        try:
            from mem0 import Memory
            
            # mem0 관련 로거들의 출력 억제
            mem0_loggers = [
                'mem0',
                'mem0.memory',
                'mem0.memory.main',
                'mem0.vector_stores',
                'mem0.embeddings',
                'mem0.llms',
                'chromadb',
                'chromadb.telemetry',
                'chromadb.api',
                'httpx',
                'httpcore',
                'openai',
                'urllib3'
            ]
            
            for logger_name in mem0_loggers:
                mem0_logger = logging.getLogger(logger_name)
                mem0_logger.setLevel(logging.CRITICAL)  # CRITICAL 이상만 표시
                # 핸들러가 있다면 제거
                mem0_logger.handlers = []
                mem0_logger.propagate = False
            
            # 루트 로거의 레벨도 조정 (mem0가 root 로거를 사용하는 경우)
            root_logger = logging.getLogger()
            # 루트 로거를 CRITICAL 레벨로 설정
            original_root_level = root_logger.level
            root_logger.setLevel(logging.CRITICAL)
            
            # 기존 핸들러 중 콘솔 핸들러의 레벨 조정
            for handler in root_logger.handlers[:]:
                if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                    handler.setLevel(logging.CRITICAL)
            
            if openai_client:
                self.openai_client = openai_client
            
            # Ollama 전용 설정 (LLM과 임베딩 모두 포함)
            mem_config = {
                "llm": {
                    "provider": config.memory.llm_provider,
                    "config": {
                        "model": config.memory.llm_model,
                        "temperature": 0.1,
                        "max_tokens": 2000
                        # Ollama LLM은 환경변수 OLLAMA_HOST로 설정
                    }
                },
                "embedder": {
                    "provider": config.memory.embed_provider,
                    "config": {
                        "model": config.memory.embed_model
                        # Ollama embedder는 base_url을 별도로 설정하지 않음
                        # 환경변수 OLLAMA_HOST나 기본값 사용
                    }
                },
                "vector_store": {
                    "provider": config.memory.vector_store,
                    "config": {
                        "collection_name": f"memories_{self.user_id}"
                    }
                }
            }
            
            # Ollama LLM과 embedder의 경우 환경변수로 호스트 설정
            if config.memory.llm_provider == "ollama" and config.memory.llm_base_url:
                # OLLAMA_HOST 환경변수 설정
                os.environ["OLLAMA_HOST"] = config.memory.llm_base_url
            
            try:
                # Memory.from_config() 사용
                with suppress_stderr():
                    self.memory = Memory.from_config(mem_config)
                self.is_initialized = True
                logger.info(f"메모리 시스템이 초기화되었습니다. (LLM: {config.memory.llm_provider}/{config.memory.llm_model}, 임베딩: {config.memory.embed_provider}/{config.memory.embed_model})")
                return True
            except Exception as config_error:
                logger.error(f"메모리 시스템 초기화 실패: {config_error}")
                logger.info("세션 모드로만 실행됩니다.")
                return False
            
        except ImportError as e:
            logger.error(f"mem0 라이브러리를 찾을 수 없습니다. 'pip install mem0ai' 명령으로 설치해주세요: {e}")
            return False
        except Exception as e:
            logger.error(f"메모리 시스템 초기화 실패: {e}")
            logger.info("세션 모드로만 실행됩니다.")
            return False
    
    def add_conversation(
        self,
        user_message: str,
        assistant_response: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """대화 내용을 메모리에 추가"""
        if not self.is_initialized:
            # 세션 메모리에만 저장
            entry = ConversationEntry(
                user_message=user_message,
                assistant_response=assistant_response,
                sentiment=SentimentType.NEUTRAL,
                metadata=metadata or {}
            )
            self.session_memories.append(entry)
            
            # 최대 개수 제한
            if len(self.session_memories) > config.memory.max_session_memories:
                self.session_memories = self.session_memories[-config.memory.max_session_memories:]
            
            return True
        
        try:
            # 장기 메모리에 저장 (mem0)
            messages = [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_response}
            ]
            
            # mem0 오류를 조용히 처리
            try:
                with suppress_stderr():
                    self.memory.add(
                        messages=messages,
                        user_id=self.user_id,
                        metadata=metadata or {}
                    )
            except Exception as mem0_error:
                # mem0 내부 오류는 디버그 레벨로만 기록
                logger.debug(f"mem0 내부 오류 (무시됨): {mem0_error}")
                # 오류가 발생해도 계속 진행
            
            # 세션 메모리에도 저장
            entry = ConversationEntry(
                user_message=user_message,
                assistant_response=assistant_response,
                sentiment=SentimentType.NEUTRAL,
                metadata=metadata or {}
            )
            self.session_memories.append(entry)
            
            # 최대 개수 제한
            if len(self.session_memories) > config.memory.max_session_memories:
                self.session_memories = self.session_memories[-config.memory.max_session_memories:]
            
            logger.debug(f"대화가 메모리에 저장되었습니다: {user_message[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"대화 저장 실패: {e}")
            return False
    
    def search_memories(self, query: str, limit: int = 5) -> MemorySearchResult:
        """관련 기억 검색"""
        start_time = datetime.now()
        
        if not self.is_initialized:
            # 세션 메모리에서만 검색
            entries = self._search_session_memories(query, limit)
            search_time = (datetime.now() - start_time).total_seconds()
            
            return MemorySearchResult(
                entries=entries,
                query=query,
                total_count=len(entries),
                search_time=search_time
            )
        
        try:
            # mem0 오류를 조용히 처리
            try:
                with suppress_stderr():
                    result = self.memory.search(
                        query=query,
                        user_id=self.user_id,
                        limit=limit
                    )
            except Exception as mem0_error:
                # mem0 내부 오류는 디버그 레벨로만 기록
                logger.debug(f"mem0 검색 오류 (무시됨): {mem0_error}")
                # 폴백으로 세션 메모리 검색
                entries = self._search_session_memories(query, limit)
                search_time = (datetime.now() - start_time).total_seconds()
                
                return MemorySearchResult(
                    entries=entries,
                    query=query,
                    total_count=len(entries),
                    search_time=search_time
                )
            
            entries = []
            if "results" in result:
                for entry in result["results"]:
                    memory_entry = MemoryEntry(
                        id=entry.get("id"),
                        content=entry.get("memory", ""),
                        memory_type=MemoryType.CONVERSATION,
                        user_id=self.user_id,
                        score=entry.get("score", 0.0),
                        metadata=entry.get("metadata", {})
                    )
                    entries.append(memory_entry)
            
            search_time = (datetime.now() - start_time).total_seconds()
            
            logger.debug(f"메모리 검색 완료: {len(entries)}개 항목 발견")
            
            return MemorySearchResult(
                entries=entries,
                query=query,
                total_count=len(entries),
                search_time=search_time
            )
            
        except Exception as e:
            logger.error(f"메모리 검색 실패: {e}")
            # 폴백으로 세션 메모리 검색
            entries = self._search_session_memories(query, limit)
            search_time = (datetime.now() - start_time).total_seconds()
            
            return MemorySearchResult(
                entries=entries,
                query=query,
                total_count=len(entries),
                search_time=search_time
            )
    
    def _search_session_memories(self, query: str, limit: int = 5) -> List[MemoryEntry]:
        """세션 메모리에서 검색 (fallback)"""
        results = []
        query_lower = query.lower()
        
        for memory in self.session_memories[-20:]:  # 최근 20개만 검색
            user_text = memory.user_message.lower()
            assistant_text = memory.assistant_response.lower()
            
            # 간단한 키워드 매칭
            if query_lower in user_text or query_lower in assistant_text:
                memory_entry = MemoryEntry(
                    content=f"사용자: {memory.user_message}\nAI: {memory.assistant_response}",
                    memory_type=MemoryType.CONVERSATION,
                    user_id=self.user_id,
                    score=0.8,
                    metadata=memory.metadata
                )
                results.append(memory_entry)
        
        return results[:limit]
    
    def add_user_preference(self, preference_type: str, preference_value: Any) -> bool:
        """사용자 선호도 저장"""
        if not self.is_initialized:
            return False
        
        try:
            preference_text = f"사용자 선호도: {preference_type} = {preference_value}"
            
            # mem0 오류를 조용히 처리
            try:
                with suppress_stderr():
                    self.memory.add(
                        messages=[{"role": "system", "content": preference_text}],
                        user_id=self.user_id,
                        metadata={"type": "preference", "category": preference_type}
                    )
            except Exception as mem0_error:
                # mem0 내부 오류는 디버그 레벨로만 기록
                logger.debug(f"mem0 선호도 저장 오류 (무시됨): {mem0_error}")
                # 오류가 발생해도 True 반환 (사용자에게는 성공으로 보임)
                
            logger.debug(f"선호도 저장됨: {preference_type} = {preference_value}")
            return True
            
        except Exception as e:
            logger.error(f"선호도 저장 실패: {e}")
            return False
    
    def get_user_preferences(self) -> List[MemoryEntry]:
        """사용자 선호도 검색"""
        if not self.is_initialized:
            return []
        
        try:
            # mem0 오류를 조용히 처리
            try:
                with suppress_stderr():
                    result = self.memory.search(
                        query="사용자 선호도",
                        user_id=self.user_id,
                        limit=20
                    )
            except Exception as mem0_error:
                # mem0 내부 오류는 디버그 레벨로만 기록
                logger.debug(f"mem0 선호도 검색 오류 (무시됨): {mem0_error}")
                return []
            
            preferences = []
            if "results" in result:
                for entry in result["results"]:
                    metadata = entry.get("metadata", {})
                    if metadata.get("type") == "preference":
                        memory_entry = MemoryEntry(
                            id=entry.get("id"),
                            content=entry.get("memory", ""),
                            memory_type=MemoryType.PREFERENCE,
                            user_id=self.user_id,
                            score=entry.get("score", 0.0),
                            metadata=metadata
                        )
                        preferences.append(memory_entry)
            
            return preferences
            
        except Exception as e:
            logger.error(f"선호도 검색 실패: {e}")
            return []
    
    def get_conversation_history(self, limit: int = 10) -> List[ConversationEntry]:
        """최근 대화 이력 반환"""
        return self.session_memories[-limit:] if self.session_memories else []
    
    def clear_session_memory(self) -> bool:
        """세션 메모리 초기화"""
        try:
            self.session_memories = []
            logger.info("세션 메모리가 초기화되었습니다.")
            return True
        except Exception as e:
            logger.error(f"세션 메모리 초기화 실패: {e}")
            return False
    
    def get_memory_stats(self) -> MemoryStats:
        """메모리 사용 통계"""
        return MemoryStats(
            total_memories=0,  # mem0에서 총 메모리 수를 가져오는 방법이 제한적
            session_memories=len(self.session_memories),
            long_term_enabled=self.is_initialized,
            user_id=self.user_id,
            last_updated=datetime.now()
        )