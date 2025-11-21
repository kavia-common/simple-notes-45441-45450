from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any


@dataclass
class Note:
    """
    Internal data model for a Note entity used within the application.

    This model represents the persisted structure and is converted
    to and from Pydantic schemas at the API boundary.
    """
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Note":
        """Create a Note from a dict persisted in JSON storage."""
        return Note(
            id=int(data["id"]),
            title=str(data.get("title", "")),
            content=str(data.get("content", "")),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Note to a serializable dict for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
