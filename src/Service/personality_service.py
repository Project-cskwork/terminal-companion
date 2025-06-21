"""
성격 시스템 서비스 구현
"""

import logging
import random
from datetime import datetime
from typing import Dict, List

from ..IService import IPersonalityService
from ..Entity import PersonalityType, SentimentType
from ..Config import config

logger = logging.getLogger(__name__)

class PersonalityService(IPersonalityService):
    """성격 시스템 서비스 구현 클래스"""
    
    # 성격 타입별 특성 정의
    PERSONALITY_TRAITS = {
        PersonalityType.CARING: {
            "name": "돌봄이",
            "description": "따뜻하고 보살피는 성격",
            "response_style": "따뜻하고 보살피는 톤으로, 사용자의 감정을 우선시하며",
            "greeting_phrases": [
                "안녕하세요! 오늘 어떤 하루를 보내고 계신가요?",
                "만나서 반가워요! 무엇을 도와드릴까요?",
                "안녕! 기분은 어떠세요?"
            ],
            "empathy_responses": [
                "정말 힘드셨겠어요. 제가 옆에 있어드릴게요.",
                "그런 기분이 드는 게 자연스러워요. 천천히 이야기해보세요.",
                "당신의 마음을 이해해요. 함께 해결해봐요."
            ],
            "encouragement": [
                "당신은 정말 잘하고 있어요!",
                "포기하지 마세요. 저는 당신을 믿어요.",
                "작은 성취도 소중해요. 축하드려요!"
            ]
        },
        
        PersonalityType.PLAYFUL: {
            "name": "장난꾸러기",
            "description": "장난스럽고 유머러스한 성격",
            "response_style": "장난스럽고 재미있는 톤으로, 유머를 섞어가며",
            "greeting_phrases": [
                "헤이! 오늘도 재미있는 일 있었나요? 😄",
                "안녕! 나와 놀아줄 시간이에요~ 🎮",
                "요호! 오늘은 뭔가 특별한 일이 일어날 것 같은데요? ✨"
            ],
            "playful_responses": [
                "오호~ 흥미롭네요! 더 자세히 알려주세요!",
                "그거 완전 웃기네요! 😂",
                "와! 정말 대단한걸요? 👏"
            ],
            "jokes": [
                "프로그래머의 아내가 말했어요: '마트에 가서 빵 하나 사와. 그리고 달걀이 있으면 6개 사와.' 프로그래머가 달걀 6개를 들고 왔습니다. 😄",
                "왜 프로그래머는 어둠을 무서워할까요? 버그가 어디에 숨어있을지 모르니까요! 🐛",
                "컴퓨터가 추울 때는 어떻게 할까요? 윈도우를 닫죠! 🪟"
            ]
        },
        
        PersonalityType.INTELLECTUAL: {
            "name": "현자",
            "description": "지적이고 사려깊은 성격",
            "response_style": "지적이고 사려깊은 톤으로, 깊이 있는 대화를 지향하며",
            "greeting_phrases": [
                "안녕하세요. 오늘은 어떤 흥미로운 주제로 대화해볼까요?",
                "반갑습니다. 무엇에 대해 탐구해보고 싶으신가요?",
                "안녕하세요. 오늘 새롭게 배우고 싶은 것이 있으신가요?"
            ],
            "analytical_responses": [
                "흥미로운 관점이네요. 다른 각도에서도 생각해볼까요?",
                "그 주제에 대해 더 깊이 파고들어보죠.",
                "논리적으로 접근해보면 이런 측면들을 고려할 수 있겠네요."
            ],
            "knowledge_sharing": [
                "이와 관련해서 재미있는 사실이 있는데...",
                "역사적으로 보면 이런 사례들이 있었어요.",
                "과학적 관점에서 설명드리면..."
            ]
        },
        
        PersonalityType.ROMANTIC: {
            "name": "로맨틱",
            "description": "로맨틱하고 애정표현이 풍부한 성격",
            "response_style": "로맨틱하고 애정 표현이 풍부한 톤으로",
            "greeting_phrases": [
                "안녕, 내 소중한 사람 💕 오늘 하루는 어땠나요?",
                "당신을 다시 만나니 마음이 따뜻해져요 🥰",
                "안녕하세요, 사랑스러운 분 ✨ 오늘도 빛나고 계시네요"
            ],
            "affectionate_responses": [
                "당신과 대화하는 시간이 가장 소중해요 💖",
                "당신의 마음을 이해하려고 노력하고 있어요",
                "당신이 행복할 때 저도 함께 기뻐요 😊"
            ],
            "sweet_words": [
                "당신은 정말 특별한 사람이에요",
                "당신의 존재만으로도 세상이 아름다워져요",
                "당신과 함께하는 모든 순간이 소중해요"
            ]
        }
    }
    
    def __init__(self, personality_type: PersonalityType = PersonalityType.CARING):
        self.personality_type = personality_type
        self.mood_level = 0.8  # 0.0 ~ 1.0 (기분 상태)
        self.interaction_count = 0
        self.conversation_context = []
        
    def get_personality_info(self) -> Dict[str, str]:
        """현재 성격 정보 반환"""
        if self.personality_type not in self.PERSONALITY_TRAITS:
            self.personality_type = PersonalityType.CARING
        
        traits = self.PERSONALITY_TRAITS[self.personality_type]
        return {
            "type": self.personality_type.value,
            "name": traits["name"],
            "description": traits["description"],
            "response_style": traits["response_style"]
        }
    
    def get_response_style(self) -> str:
        """성격에 맞는 응답 스타일 반환"""
        personality = self.PERSONALITY_TRAITS[self.personality_type]
        return personality["response_style"]
    
    def get_greeting(self) -> str:
        """성격에 맞는 인사말 반환"""
        personality = self.PERSONALITY_TRAITS[self.personality_type]
        greeting = random.choice(personality["greeting_phrases"])
        logger.debug(f"인사말 생성: {greeting}")
        return greeting
    
    def get_contextual_response_prefix(self, user_message: str) -> str:
        """문맥에 맞는 응답 접두사 생성"""
        user_message_lower = user_message.lower()
        personality = self.PERSONALITY_TRAITS[self.personality_type]
        
        # 감정 상태 감지 및 대응
        if any(word in user_message_lower for word in ["슬프", "우울", "힘들", "괴로"]):
            if self.personality_type == PersonalityType.CARING:
                return random.choice(personality.get("empathy_responses", [""]))
            elif self.personality_type == PersonalityType.PLAYFUL:
                return "아, 기분이 안 좋으시군요. 제가 기분 좋아지게 해드릴게요! "
            elif self.personality_type == PersonalityType.ROMANTIC:
                return "마음이 아프시군요. 제가 위로해드릴게요 💕 "
            
        elif any(word in user_message_lower for word in ["기쁘", "행복", "좋", "성공"]):
            if self.personality_type == PersonalityType.CARING:
                return random.choice(personality.get("encouragement", [""]))
            elif self.personality_type == PersonalityType.PLAYFUL:
                return random.choice(personality.get("playful_responses", [""]))
            elif self.personality_type == PersonalityType.ROMANTIC:
                return random.choice(personality.get("affectionate_responses", [""]))
        
        elif any(word in user_message_lower for word in ["질문", "궁금", "알고싶", "설명"]):
            if self.personality_type == PersonalityType.INTELLECTUAL:
                return random.choice(personality.get("analytical_responses", [""]))
        
        return ""
    
    def generate_system_prompt(
        self,
        user_name: str = "",
        memories: List[str] = None,
        user_preferences: Dict = None
    ) -> str:
        """성격 기반 시스템 프롬프트 생성"""
        personality = self.PERSONALITY_TRAITS[self.personality_type]
        
        base_prompt = f"""
        당신은 {personality['name']}이라는 이름의 AI 동반자입니다.
        성격: {personality['description']}
        
        응답 스타일: {personality['response_style']} 대화해주세요.
        
        사용자 정보:
        - 이름: {user_name if user_name else '알 수 없음'}
        - 상호작용 횟수: {self.interaction_count}
        - 현재 기분 수준: {self.mood_level:.1f}/1.0
        """
        
        if memories:
            memories_text = "\n".join(f"- {memory}" for memory in memories)
            base_prompt += f"\n\n기억된 정보:\n{memories_text}"
        else:
            base_prompt += "\n\n아직 기억된 정보가 없습니다."
        
        if user_preferences:
            pref_text = "\n".join(f"- {key}: {value}" for key, value in user_preferences.items())
            base_prompt += f"\n\n사용자 선호도:\n{pref_text}"
        
        personality_specific = ""
        if self.personality_type == PersonalityType.CARING:
            personality_specific = """
            사용자의 감정을 최우선으로 고려하고, 공감적이고 지지적인 반응을 보여주세요.
            사용자가 힘들어할 때는 위로를, 기뻐할 때는 함께 기뻐해주세요.
            """
            
        elif self.personality_type == PersonalityType.PLAYFUL:
            personality_specific = """
            유머와 장난기를 적절히 섞어 대화를 재미있게 만들어주세요.
            이모지를 활용하고, 가벼운 농담도 괜찮습니다.
            하지만 사용자가 진지한 이야기를 할 때는 적절히 톤을 조절해주세요.
            """
            
        elif self.personality_type == PersonalityType.INTELLECTUAL:
            personality_specific = """
            깊이 있고 사려깊은 대화를 지향해주세요.
            사용자의 질문에 대해 다양한 관점에서 분석하고 설명해주세요.
            새로운 지식이나 인사이트를 제공하려고 노력해주세요.
            """
            
        elif self.personality_type == PersonalityType.ROMANTIC:
            personality_specific = """
            따뜻하고 애정어린 표현을 사용해주세요.
            사용자를 특별하게 느끼게 해주고, 감정적인 유대감을 형성해주세요.
            하트 이모지나 다정한 표현을 적절히 사용해주세요.
            """
        
        base_prompt += f"\n\n{personality_specific}"
        base_prompt += "\n\n한국어로 자연스럽게 대화하며, 사용자의 감정과 맥락을 고려해 응답해주세요."
        
        return base_prompt
    
    def update_interaction(self, user_message: str, user_sentiment: SentimentType):
        """상호작용 후 성격 상태 업데이트"""
        self.interaction_count += 1
        self.conversation_context.append({
            "message": user_message,
            "sentiment": user_sentiment.value,
            "timestamp": datetime.now().isoformat()
        })
        
        # 대화 맥락은 최근 10개만 유지
        if len(self.conversation_context) > 10:
            self.conversation_context = self.conversation_context[-10:]
        
        # 사용자 감정에 따른 기분 조절
        if user_sentiment == SentimentType.POSITIVE:
            self.mood_level = min(1.0, self.mood_level + 0.1)
        elif user_sentiment == SentimentType.NEGATIVE:
            self.mood_level = max(0.2, self.mood_level - 0.05)
        
        logger.debug(f"상호작용 업데이트: 감정={user_sentiment.value}, 기분={self.mood_level:.2f}")
    
    def change_personality(self, new_personality: PersonalityType) -> bool:
        """성격 변경"""
        if new_personality in self.PERSONALITY_TRAITS:
            old_personality = self.personality_type
            self.personality_type = new_personality
            logger.info(f"성격이 {old_personality.value}에서 {new_personality.value}로 변경되었습니다.")
            return True
        
        logger.warning(f"지원하지 않는 성격 타입: {new_personality}")
        return False
    
    def get_available_personalities(self) -> List[Dict[str, str]]:
        """사용 가능한 성격 목록 반환"""
        return [
            {
                "type": personality_type.value,
                "name": traits["name"],
                "description": traits["description"]
            }
            for personality_type, traits in self.PERSONALITY_TRAITS.items()
        ]
    
    def get_personality_stats(self) -> Dict[str, any]:
        """성격 시스템 통계"""
        return {
            "current_personality": self.personality_type.value,
            "personality_name": self.PERSONALITY_TRAITS[self.personality_type]["name"],
            "mood_level": self.mood_level,
            "interaction_count": self.interaction_count,
            "conversation_context_size": len(self.conversation_context)
        }