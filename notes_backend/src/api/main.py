from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers_notes import router as notes_router
from . import storage

app = FastAPI(
    title="Simple Notes API",
    description="A minimal API to create, view, edit, and delete notes.\n\n"
                "Endpoints:\n"
                "- GET/POST /notes\n"
                "- GET/PUT/DELETE /notes/{id}",
    version="1.0.0",
    contact={"name": "Notes Backend", "url": "https://example.com"},
    license_info={"name": "MIT"},
    openapi_tags=[
        {"name": "Notes", "description": "Operations for managing notes."},
        {"name": "Health", "description": "Service health monitoring."},
    ],
)

# Allow any origin for quick testing in preview environments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize storage and seed sample data when the app starts
@app.on_event("startup")
def _on_startup():
    storage.init_storage()

# Register routers
app.include_router(notes_router)


@app.get("/", tags=["Health"], summary="Health Check", description="Simple health check endpoint.")
def health_check():
    """
    Health check endpoint.

    Returns:
        dict: A JSON object indicating service health.
    """
    return {"message": "Healthy"}
