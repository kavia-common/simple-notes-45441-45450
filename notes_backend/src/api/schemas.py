from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class NoteCreate(BaseModel):
    """Schema for creating a new note."""
    title: str = Field(..., min_length=1, max_length=200, description="Title of the note (1-200 chars).")
    content: str = Field("", max_length=5000, description="Content/body of the note (max 5000 chars).")


# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Schema for updating an existing note; fields are optional but must meet constraints if provided."""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Updated title for the note.")
    content: Optional[str] = Field(None, max_length=5000, description="Updated content for the note.")


# PUBLIC_INTERFACE
class NoteOut(BaseModel):
    """Schema returned by the API representing a note."""
    id: int = Field(..., description="Unique identifier of the note.")
    title: str = Field(..., description="Title of the note.")
    content: str = Field(..., description="Content/body of the note.")
    created_at: datetime = Field(..., description="Timestamp when the note was created (ISO 8601).")
    updated_at: datetime = Field(..., description="Timestamp when the note was last updated (ISO 8601).")
