from __future__ import annotations

import json
import os
from datetime import datetime
from threading import RLock
from typing import Dict, List, Optional

from .models import Note

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "notes_data.json")

_lock = RLock()


def _now() -> datetime:
    return datetime.utcnow()


def _load_raw() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        # If file is corrupted, start fresh in-memory
        return []


def _save_raw(items: List[Dict]) -> None:
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def _seed_if_empty() -> None:
    """Seed the storage with sample notes when empty for quick manual verification."""
    items = _load_raw()
    if items:
        return
    now = _now().isoformat()
    sample = [
        {"id": 1, "title": "Welcome to Notes", "content": "This is your first note.", "created_at": now, "updated_at": now},
        {"id": 2, "title": "Tips", "content": "Use POST /notes to add, PUT to update, DELETE to remove.", "created_at": now, "updated_at": now},
    ]
    _save_raw(sample)


def _next_id(existing: List[Dict]) -> int:
    if not existing:
        return 1
    return max(int(n.get("id", 0)) for n in existing) + 1


# PUBLIC_INTERFACE
def init_storage() -> None:
    """Initialize storage, seeding sample data if necessary."""
    with _lock:
        _seed_if_empty()


# PUBLIC_INTERFACE
def list_notes() -> List[Note]:
    """Return all notes as Note models."""
    with _lock:
        return [Note.from_dict(n) for n in _load_raw()]


# PUBLIC_INTERFACE
def get_note(note_id: int) -> Optional[Note]:
    """Get a single note by id, or None if missing."""
    with _lock:
        for n in _load_raw():
            if int(n.get("id")) == note_id:
                return Note.from_dict(n)
        return None


# PUBLIC_INTERFACE
def create_note(title: str, content: str) -> Note:
    """Create a new note and persist it."""
    with _lock:
        items = _load_raw()
        new_id = _next_id(items)
        now = _now().isoformat()
        record = {"id": new_id, "title": title, "content": content, "created_at": now, "updated_at": now}
        items.append(record)
        _save_raw(items)
        return Note.from_dict(record)


# PUBLIC_INTERFACE
def update_note(note_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Note]:
    """Update note fields; returns updated note or None if not found."""
    with _lock:
        items = _load_raw()
        for idx, n in enumerate(items):
            if int(n.get("id")) == note_id:
                if title is not None:
                    n["title"] = title
                if content is not None:
                    n["content"] = content
                n["updated_at"] = _now().isoformat()
                items[idx] = n
                _save_raw(items)
                return Note.from_dict(n)
        return None


# PUBLIC_INTERFACE
def delete_note(note_id: int) -> bool:
    """Delete a note by id; returns True if deleted, False if not found."""
    with _lock:
        items = _load_raw()
        new_items = [n for n in items if int(n.get("id")) != note_id]
        if len(new_items) == len(items):
            return False
        _save_raw(new_items)
        return True
