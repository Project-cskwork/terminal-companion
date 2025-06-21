"""
사용자 프로필 엔티티 정의
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

class PersonalityType(Enum):
    """성격 유형"""
    CARING = "caring"
    PLAYFUL = "playful"
    INTELLECTUAL = "intellectual"
    ROMANTIC = "romantic"

@dataclass
class UserPreference:
    """사용자 선호도"""
    category: str
    value: str
    confidence: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "category": self.category,
            "value": self.value,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreference':
        """딕셔너리에서 생성"""
        return cls(
            category=data["category"],
            value=data["value"],
            confidence=data.get("confidence", 1.0),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat()))
        )

@dataclass
class UserStats:
    """사용자 통계"""
    total_conversations: int = 0
    total_session_time: float = 0.0
    favorite_personality: Optional[PersonalityType] = None
    most_used_commands: List[str] = field(default_factory=list)
    last_active: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "total_conversations": self.total_conversations,
            "total_session_time": self.total_session_time,
            "favorite_personality": self.favorite_personality.value if self.favorite_personality else None,
            "most_used_commands": self.most_used_commands,
            "last_active": self.last_active.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserStats':
        """딕셔너리에서 생성"""
        favorite_personality = None
        if data.get("favorite_personality"):
            favorite_personality = PersonalityType(data["favorite_personality"])
        
        return cls(
            total_conversations=data.get("total_conversations", 0),
            total_session_time=data.get("total_session_time", 0.0),
            favorite_personality=favorite_personality,
            most_used_commands=data.get("most_used_commands", []),
            last_active=datetime.fromisoformat(data.get("last_active", datetime.now().isoformat()))
        )

@dataclass
class UserProfile:
    """사용자 프로필 엔티티"""
    user_id: str
    name: str = ""
    preferred_personality: PersonalityType = PersonalityType.CARING
    preferences: Dict[str, UserPreference] = field(default_factory=dict)
    stats: UserStats = field(default_factory=UserStats)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_preference(self, category: str, value: str, confidence: float = 1.0):
        """선호도 추가 또는 업데이트"""
        key = f"{category}_{value}"
        if key in self.preferences:
            # 기존 선호도 업데이트
            self.preferences[key].confidence = max(self.preferences[key].confidence, confidence)
            self.preferences[key].updated_at = datetime.now()
        else:
            # 새로운 선호도 추가
            self.preferences[key] = UserPreference(
                category=category,
                value=value,
                confidence=confidence
            )
        
        self.updated_at = datetime.now()
    
    def get_preferences_by_category(self, category: str) -> List[UserPreference]:
        """카테고리별 선호도 반환"""
        return [pref for pref in self.preferences.values() if pref.category == category]
    
    def update_stats(self, conversations_increment: int = 1, session_time_increment: float = 0.0):
        """통계 업데이트"""
        self.stats.total_conversations += conversations_increment
        self.stats.total_session_time += session_time_increment
        self.stats.last_active = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "preferred_personality": self.preferred_personality.value,
            "preferences": {key: pref.to_dict() for key, pref in self.preferences.items()},
            "stats": self.stats.to_dict(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        """딕셔너리에서 생성"""
        preferences = {}
        for key, pref_data in data.get("preferences", {}).items():
            preferences[key] = UserPreference.from_dict(pref_data)
        
        return cls(
            user_id=data["user_id"],
            name=data.get("name", ""),
            preferred_personality=PersonalityType(data.get("preferred_personality", "caring")),
            preferences=preferences,
            stats=UserStats.from_dict(data.get("stats", {})),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
            metadata=data.get("metadata", {})
        )