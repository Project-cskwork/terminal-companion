"""
메모리 관련 엔티티 정의
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

class MemoryType(Enum):
    """메모리 유형"""
    CONVERSATION = "conversation"
    PREFERENCE = "preference"
    FACT = "fact"
    EMOTION = "emotion"

@dataclass
class MemoryEntry:
    """메모리 항목 엔티티"""
    id: Optional[str] = None
    content: str = ""
    memory_type: MemoryType = MemoryType.CONVERSATION
    user_id: str = "default_user"
    score: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "id": self.id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "user_id": self.user_id,
            "score": self.score,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """딕셔너리에서 생성"""
        return cls(
            id=data.get("id"),
            content=data.get("content", ""),
            memory_type=MemoryType(data.get("memory_type", "conversation")),
            user_id=data.get("user_id", "default_user"),
            score=data.get("score", 0.0),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            metadata=data.get("metadata", {})
        )

@dataclass
class MemorySearchResult:
    """메모리 검색 결과"""
    entries: List[MemoryEntry] = field(default_factory=list)
    query: str = ""
    total_count: int = 0
    search_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "entries": [entry.to_dict() for entry in self.entries],
            "query": self.query,
            "total_count": self.total_count,
            "search_time": self.search_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemorySearchResult':
        """딕셔너리에서 생성"""
        entries = [MemoryEntry.from_dict(entry_data) for entry_data in data.get("entries", [])]
        return cls(
            entries=entries,
            query=data.get("query", ""),
            total_count=data.get("total_count", 0),
            search_time=data.get("search_time", 0.0)
        )

@dataclass
class MemoryStats:
    """메모리 통계"""
    total_memories: int = 0
    session_memories: int = 0
    long_term_enabled: bool = False
    user_id: str = "default_user"
    last_updated: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "total_memories": self.total_memories,
            "session_memories": self.session_memories,
            "long_term_enabled": self.long_term_enabled,
            "user_id": self.user_id,
            "last_updated": self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryStats':
        """딕셔너리에서 생성"""
        return cls(
            total_memories=data.get("total_memories", 0),
            session_memories=data.get("session_memories", 0),
            long_term_enabled=data.get("long_term_enabled", False),
            user_id=data.get("user_id", "default_user"),
            last_updated=datetime.fromisoformat(data.get("last_updated", datetime.now().isoformat()))
        )