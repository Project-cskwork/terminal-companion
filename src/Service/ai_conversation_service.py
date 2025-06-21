"""
AI 대화 서비스 구현 - 다중 제공자 지원
"""

import logging
import json
import httpx
import requests
from datetime import datetime
from typing import List, Dict, Optional

from ..IService import IAIConversationService
from ..Entity import ConversationEntry, SentimentType
from ..Config import config

logger = logging.getLogger(__name__)

class AIConversationService(IAIConversationService):
    """AI 대화 서비스 구현 클래스 - OpenAI, OpenRouter, Ollama 지원"""
    
    def __init__(self):
        self.openai_client = None
        self.is_initialized = False
        self.current_provider = config.ai.provider
        self.conversation_stats = {
            "total_conversations": 0,
            "total_tokens_used": 0,
            "last_conversation": None
        }
    
    def initialize(self, api_key: Optional[str] = None) -> bool:
        """AI 클라이언트 초기화"""
        try:
            if self.current_provider == 'openai':
                return self._initialize_openai(api_key)
            elif self.current_provider == 'openrouter':
                return self._initialize_openrouter(api_key)
            elif self.current_provider == 'ollama':
                return self._initialize_ollama()
            else:
                logger.error(f"지원하지 않는 AI 제공자: {self.current_provider}")
                return False
                
        except Exception as e:
            logger.error(f"AI 클라이언트 초기화 실패: {e}")
            return False
    
    def _initialize_openai(self, api_key: Optional[str] = None) -> bool:
        """OpenAI 클라이언트 초기화"""
        try:
            from openai import OpenAI
            
            if not api_key:
                api_key = config.ai.openai_api_key
            
            if not api_key:
                logger.warning("OpenAI API 키가 설정되지 않았습니다.")
                return False
            
            self.openai_client = OpenAI(api_key=api_key)
            self.is_initialized = True
            logger.info("OpenAI 클라이언트가 성공적으로 초기화되었습니다.")
            return True
            
        except ImportError as e:
            logger.error(f"OpenAI 라이브러리를 찾을 수 없습니다: {e}")
            return False
    
    def _initialize_openrouter(self, api_key: Optional[str] = None) -> bool:
        """OpenRouter 클라이언트 초기화"""
        try:
            if not api_key:
                api_key = config.ai.openrouter_api_key
            
            if not api_key:
                logger.warning("OpenRouter API 키가 설정되지 않았습니다.")
                return False
            
            self.is_initialized = True
            logger.info("OpenRouter 클라이언트가 성공적으로 초기화되었습니다.")
            return True
            
        except Exception as e:
            logger.error(f"OpenRouter 초기화 실패: {e}")
            return False
    
    def _initialize_ollama(self) -> bool:
        """Ollama 클라이언트 초기화"""
        try:
            # Ollama 서버가 실행 중인지 확인
            response = requests.get(f"{config.ai.ollama_base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                self.is_initialized = True
                logger.info("Ollama 서버 연결 성공")
                return True
            else:
                logger.warning("Ollama 서버에 연결할 수 없습니다.")
                return False
                
        except Exception as e:
            logger.error(f"Ollama 초기화 실패: {e}")
            return False
    
    def generate_response(
        self,
        user_message: str,
        system_prompt: str,
        conversation_history: Optional[List[ConversationEntry]] = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> Optional[str]:
        """AI 응답 생성"""
        if not self.is_initialized:
            return self._fallback_response(user_message)
        
        # 설정에서 기본값 사용
        if temperature is None:
            temperature = config.ai.temperature
        if max_tokens is None:
            max_tokens = config.ai.max_tokens
        
        try:
            if self.current_provider == 'openai':
                return self._generate_openai_response(
                    user_message, system_prompt, conversation_history, temperature, max_tokens
                )
            elif self.current_provider == 'openrouter':
                return self._generate_openrouter_response(
                    user_message, system_prompt, conversation_history, temperature, max_tokens
                )
            elif self.current_provider == 'ollama':
                return self._generate_ollama_response(
                    user_message, system_prompt, conversation_history, temperature, max_tokens
                )
        except Exception as e:
            logger.error(f"AI 응답 생성 실패: {e}")
            return self._fallback_response(user_message)
    
    def _generate_openai_response(
        self, user_message: str, system_prompt: str, 
        conversation_history: Optional[List[ConversationEntry]], 
        temperature: float, max_tokens: int
    ) -> Optional[str]:
        """OpenAI API를 사용한 응답 생성"""
        messages = self._build_messages(system_prompt, conversation_history, user_message)
        
        response = self.openai_client.chat.completions.create(
            model=config.ai.openai_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            frequency_penalty=0.1,
            presence_penalty=0.1
        )
        
        assistant_response = response.choices[0].message.content
        
        # 통계 업데이트
        self.conversation_stats["total_conversations"] += 1
        self.conversation_stats["total_tokens_used"] += response.usage.total_tokens
        self.conversation_stats["last_conversation"] = datetime.now().isoformat()
        
        return assistant_response
    
    def _generate_openrouter_response(
        self, user_message: str, system_prompt: str,
        conversation_history: Optional[List[ConversationEntry]],
        temperature: float, max_tokens: int
    ) -> Optional[str]:
        """OpenRouter API를 사용한 응답 생성"""
        messages = self._build_messages(system_prompt, conversation_history, user_message)
        
        headers = {
            "Authorization": f"Bearer {config.ai.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/terminal-companion",
            "X-Title": "Terminal AI Companion"
        }
        
        data = {
            "model": config.ai.openrouter_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            assistant_response = result["choices"][0]["message"]["content"]
            
            # 통계 업데이트
            self.conversation_stats["total_conversations"] += 1
            if "usage" in result:
                self.conversation_stats["total_tokens_used"] += result["usage"]["total_tokens"]
            self.conversation_stats["last_conversation"] = datetime.now().isoformat()
            
            return assistant_response
        else:
            logger.error(f"OpenRouter API 오류: {response.status_code} - {response.text}")
            return None
    
    def _generate_ollama_response(
        self, user_message: str, system_prompt: str,
        conversation_history: Optional[List[ConversationEntry]],
        temperature: float, max_tokens: int
    ) -> Optional[str]:
        """Ollama API를 사용한 응답 생성"""
        messages = self._build_messages(system_prompt, conversation_history, user_message)
        
        # Ollama 형식으로 변환
        prompt = f"System: {system_prompt}\n\n"
        
        if conversation_history:
            for entry in conversation_history[-10:]:
                prompt += f"Human: {entry.user_message}\nAssistant: {entry.assistant_response}\n\n"
        
        prompt += f"Human: {user_message}\nAssistant:"
        
        data = {
            "model": "gemma3:1b",  # 실제 실행중인 모델 사용
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        response = requests.post(
            f"{config.ai.ollama_base_url}/api/generate",
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            assistant_response = result.get("response", "")
            
            # 통계 업데이트
            self.conversation_stats["total_conversations"] += 1
            self.conversation_stats["last_conversation"] = datetime.now().isoformat()
            
            return assistant_response
        else:
            logger.error(f"Ollama API 오류: {response.status_code} - {response.text}")
            return None
    
    def _build_messages(
        self, system_prompt: str, 
        conversation_history: Optional[List[ConversationEntry]], 
        user_message: str
    ) -> List[Dict[str, str]]:
        """대화 메시지 구성"""
        messages = [{"role": "system", "content": system_prompt}]
        
        # 대화 이력 추가 (최근 10개만)
        if conversation_history:
            for entry in conversation_history[-10:]:
                messages.append({"role": "user", "content": entry.user_message})
                messages.append({"role": "assistant", "content": entry.assistant_response})
        
        # 현재 사용자 메시지 추가
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def _fallback_response(self, user_message: str) -> str:
        """AI 사용 불가 시 기본 응답"""
        user_lower = user_message.lower()
        
        # 감정 키워드 기반 응답
        if any(word in user_lower for word in ["안녕", "hello", "hi"]):
            return "안녕하세요! 만나서 반가워요. AI 서비스에 연결할 수 없지만 여전히 당신과 대화하고 싶어요."
        
        elif any(word in user_lower for word in ["슬프", "우울", "힘들"]):
            return "힘든 시간이시군요. 비록 AI 서비스가 연결되지 않았지만, 제가 여기 있어서 당신의 이야기를 들어드릴 수 있어요."
        
        elif any(word in user_lower for word in ["기쁘", "행복", "좋"]):
            return "기분이 좋으시다니 저도 함께 기뻐요! 더 자세한 이야기를 들려주세요."
        
        elif any(word in user_lower for word in ["고마워", "감사"]):
            return "천만에요! 언제든지 도움이 필요하시면 말씀해주세요."
        
        elif any(word in user_lower for word in ["안녕히", "bye", "goodbye"]):
            return "안녕히 가세요! 좋은 하루 보내시고, 다음에 또 만나요!"
        
        elif "?" in user_message or any(word in user_lower for word in ["뭐", "무엇", "왜", "어떻게"]):
            return "궁금한 것이 있으시군요. AI 서비스가 연결되면 더 자세한 답변을 드릴 수 있을 텐데, 지금은 제한적인 응답만 가능해요."
        
        else:
            responses = [
                "흥미로운 이야기네요. 더 자세히 말씀해주세요.",
                "그런 일이 있으셨군요. 어떤 기분이셨나요?",
                "당신의 이야기를 듣고 있어요. 계속해주세요.",
                "AI 연결이 안 되어 있지만, 여전히 당신과 대화하고 싶어요.",
                "제한적이지만 당신의 동반자가 되어드리고 싶어요."
            ]
            import random
            return random.choice(responses)
    
    def analyze_sentiment(self, text: str) -> SentimentType:
        """간단한 감정 분석 (키워드 기반)"""
        text_lower = text.lower()
        
        positive_words = ["기쁘", "행복", "좋", "사랑", "고마워", "완벽", "최고", "성공", "축하"]
        negative_words = ["슬프", "우울", "힘들", "괴로", "화나", "짜증", "실망", "걱정", "두렵"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return SentimentType.POSITIVE
        elif negative_count > positive_count:
            return SentimentType.NEGATIVE
        else:
            return SentimentType.NEUTRAL
    
    def extract_preferences(self, user_message: str) -> Dict[str, str]:
        """사용자 메시지에서 선호도 추출"""
        preferences = {}
        message_lower = user_message.lower()
        
        # 음식 선호도
        if any(word in message_lower for word in ["좋아", "싫어", "선호"]):
            if any(food in message_lower for food in ["피자", "치킨", "한식", "중식", "일식", "양식"]):
                for food in ["피자", "치킨", "한식", "중식", "일식", "양식"]:
                    if food in message_lower:
                        if "좋아" in message_lower:
                            preferences[f"음식_{food}"] = "좋아함"
                        elif "싫어" in message_lower:
                            preferences[f"음식_{food}"] = "싫어함"
        
        # 활동 선호도
        if any(word in message_lower for word in ["좋아", "취미", "관심"]):
            activities = ["영화", "음악", "독서", "운동", "게임", "여행", "요리"]
            for activity in activities:
                if activity in message_lower:
                    preferences[f"활동_{activity}"] = "관심있음"
        
        # 성격 선호도
        personality_hints = {
            "재미있": "playful",
            "장난": "playful", 
            "유머": "playful",
            "따뜻": "caring",
            "돌봄": "caring",
            "지적": "intellectual",
            "똑똑": "intellectual",
            "로맨틱": "romantic",
            "사랑": "romantic"
        }
        
        for hint, personality in personality_hints.items():
            if hint in message_lower:
                preferences["선호_성격"] = personality
        
        if preferences:
            logger.debug(f"선호도 추출됨: {preferences}")
        
        return preferences
    
    def get_conversation_stats(self) -> Dict[str, any]:
        """대화 통계 반환"""
        return self.conversation_stats.copy()
    
    def set_provider(self, provider: str) -> bool:
        """AI 제공자 변경"""
        valid_providers = ["openai", "openrouter", "ollama"]
        
        if provider in valid_providers:
            self.current_provider = provider
            self.is_initialized = False  # 재초기화 필요
            logger.info(f"AI 제공자가 {provider}로 변경되었습니다.")
            return True
        
        logger.warning(f"지원하지 않는 제공자: {provider}")
        return False
    
    def set_model(self, model_name: str) -> bool:
        """사용할 모델 변경"""
        if self.current_provider == "openai":
            valid_models = ["gpt-4o-mini", "gpt-4o", "gpt-4", "gpt-3.5-turbo"]
            if model_name in valid_models:
                config.ai.openai_model = model_name
                logger.info(f"OpenAI 모델이 {model_name}로 변경되었습니다.")
                return True
        
        elif self.current_provider == "openrouter":
            # OpenRouter 모델은 더 유연하게 허용
            config.ai.openrouter_model = model_name
            logger.info(f"OpenRouter 모델이 {model_name}로 변경되었습니다.")
            return True
        
        elif self.current_provider == "ollama":
            # Ollama 모델도 유연하게 허용
            config.ai.ollama_model = model_name
            logger.info(f"Ollama 모델이 {model_name}로 변경되었습니다.")
            return True
        
        logger.warning(f"지원하지 않는 모델: {model_name}")
        return False
    
    def get_available_models(self) -> List[str]:
        """현재 제공자의 사용 가능한 모델 목록"""
        if self.current_provider == "openai":
            return ["gpt-4o-mini", "gpt-4o", "gpt-4", "gpt-3.5-turbo"]
        elif self.current_provider == "openrouter":
            return [
                "openai/gpt-4o-mini",
                "openai/gpt-4o", 
                "openai/gpt-4-turbo",
                "anthropic/claude-3-sonnet",
                "anthropic/claude-3-haiku",
                "meta-llama/llama-3.1-8b-instruct",
                "meta-llama/llama-3.1-70b-instruct",
                "google/gemini-pro"
            ]
        elif self.current_provider == "ollama":
            try:
                # 실제 설치된 모델 목록 가져오기
                response = requests.get(f"{config.ai.ollama_base_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    return [model["name"] for model in models]
                else:
                    return ["gemma3:1b", "gemma2:2b", "llama3.2", "llama3.1", "mistral", "codellama", "phi3"]
            except:
                return ["gemma3:1b", "gemma2:2b", "llama3.2", "llama3.1", "mistral", "codellama", "phi3"]
        
        return []
    
    def get_available_providers(self) -> List[str]:
        """사용 가능한 AI 제공자 목록"""
        return ["openai", "openrouter", "ollama"]
    
    def get_current_provider(self) -> str:
        """현재 사용 중인 AI 제공자"""
        return self.current_provider
    
    def get_current_model(self) -> str:
        """현재 사용 중인 모델"""
        if self.current_provider == "openai":
            return config.ai.openai_model
        elif self.current_provider == "openrouter":
            return config.ai.openrouter_model
        elif self.current_provider == "ollama":
            return config.ai.ollama_model
        return ""
    
    def reset_stats(self) -> None:
        """통계 초기화"""
        self.conversation_stats = {
            "total_conversations": 0,
            "total_tokens_used": 0,
            "last_conversation": None
        }
        logger.info("AI 대화 통계가 초기화되었습니다.")