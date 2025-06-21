"""
대화 관련 엔티티 정의
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

class MessageRole(Enum):
    """메시지 역할"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class SentimentType(Enum):
    """감정 유형"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

@dataclass
class Message:
    """메시지 엔티티"""
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """딕셔너리에서 생성"""
        return cls(
            role=MessageRole(data["role"]),
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {})
        )

@dataclass
class ConversationEntry:
    """대화 항목 엔티티"""
    user_message: str
    assistant_response: str
    sentiment: SentimentType
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "user_message": self.user_message,
            "assistant_response": self.assistant_response,
            "sentiment": self.sentiment.value,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationEntry':
        """딕셔너리에서 생성"""
        return cls(
            user_message=data["user_message"],
            assistant_response=data["assistant_response"],
            sentiment=SentimentType(data["sentiment"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {})
        )
    
    def get_messages(self) -> List[Message]:
        """메시지 리스트로 변환"""
        return [
            Message(MessageRole.USER, self.user_message, self.timestamp, self.metadata),
            Message(MessageRole.ASSISTANT, self.assistant_response, self.timestamp, self.metadata)
        ]

@dataclass
class ConversationHistory:
    """대화 이력 엔티티"""
    entries: List[ConversationEntry] = field(default_factory=list)
    max_entries: int = 100
    
    def add_entry(self, entry: ConversationEntry):
        """대화 항목 추가"""
        self.entries.append(entry)
        
        # 최대 항목 수 초과 시 오래된 항목 제거
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]
    
    def get_recent_entries(self, limit: int = 10) -> List[ConversationEntry]:
        """최근 대화 항목 반환"""
        return self.entries[-limit:] if self.entries else []
    
    def get_messages_for_api(self, limit: int = 10) -> List[Dict[str, str]]:
        """API 호출용 메시지 형식으로 변환"""
        recent_entries = self.get_recent_entries(limit)
        messages = []
        
        for entry in recent_entries:
            messages.append({"role": "user", "content": entry.user_message})
            messages.append({"role": "assistant", "content": entry.assistant_response})
        
        return messages
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "entries": [entry.to_dict() for entry in self.entries],
            "max_entries": self.max_entries
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationHistory':
        """딕셔너리에서 생성"""
        entries = [ConversationEntry.from_dict(entry_data) for entry_data in data.get("entries", [])]
        return cls(
            entries=entries,
            max_entries=data.get("max_entries", 100)
        )