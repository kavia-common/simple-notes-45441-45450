from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status
from . import storage
from .schemas import NoteCreate, NoteUpdate, NoteOut

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.get(
    "",
    response_model=List[NoteOut],
    summary="List notes",
    description="Retrieve all notes currently stored.",
)
def list_all_notes():
    """
    List all notes.

    Returns:
        List[NoteOut]: A list of note objects.
    """
    notes = storage.list_notes()
    return [NoteOut.model_validate(n.__dict__) for n in notes]


@router.post(
    "",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Create a new note with a title and optional content.",
)
def create_new_note(payload: NoteCreate):
    """
    Create a new note.

    Parameters:
        payload (NoteCreate): The note to create with title and content.

    Returns:
        NoteOut: The created note with its generated id and timestamps.
    """
    note = storage.create_note(title=payload.title.strip(), content=payload.content or "")
    return NoteOut.model_validate(note.__dict__)


@router.get(
    "/{note_id}",
    response_model=NoteOut,
    summary="Get a note by id",
    description="Retrieve a single note by its unique id.",
)
def retrieve_note(note_id: int):
    """
    Retrieve a note.

    Parameters:
        note_id (int): ID of the note to retrieve.

    Returns:
        NoteOut: The note object.

    Raises:
        HTTPException 404: If the note does not exist.
    """
    note = storage.get_note(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteOut.model_validate(note.__dict__)


@router.put(
    "/{note_id}",
    response_model=NoteOut,
    summary="Update a note by id",
    description="Update title and/or content of an existing note.",
)
def update_existing_note(note_id: int, payload: NoteUpdate):
    """
    Update an existing note.

    Parameters:
        note_id (int): ID of the note to update.
        payload (NoteUpdate): Fields to update.

    Returns:
        NoteOut: The updated note.

    Raises:
        HTTPException 404: If the note does not exist.
    """
    note = storage.update_note(
        note_id=note_id,
        title=payload.title.strip() if payload.title is not None else None,
        content=payload.content if payload.content is not None else None,
    )
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteOut.model_validate(note.__dict__)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note by id",
    description="Delete an existing note by its unique id.",
)
def delete_existing_note(note_id: int):
    """
    Delete a note.

    Parameters:
        note_id (int): ID of the note to delete.

    Returns:
        None

    Raises:
        HTTPException 404: If the note does not exist.
    """
    deleted = storage.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return None
