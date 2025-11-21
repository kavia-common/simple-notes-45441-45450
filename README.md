# simple-notes-45441-45450

Simple Notes API (FastAPI)
- Backend container: notes_backend
- Purpose: Minimal CRUD for notes with file-backed JSON persistence.

Base URL
- Local/Preview environment usually exposes docs at /docs and schema at /openapi.json
- Example (from task context): https://vscode-internal-26880-qa.qa01.cloud.kavia.ai:3001

OpenAPI Docs
- Visit: /docs

Endpoints
- GET /notes: List notes
- POST /notes: Create note
- GET /notes/{id}: Retrieve a note by id
- PUT /notes/{id}: Update a note by id
- DELETE /notes/{id}: Delete a note by id

Data Model
- Note: { id: int, title: str, content: str, created_at: datetime, updated_at: datetime }
- notes_data.json persists in container root of notes_backend workspace

cURL Examples
Replace BASE with your server base, e.g., BASE="https://vscode-internal-26880-qa.qa01.cloud.kavia.ai:3001"

List notes
curl -s "${BASE}/notes" | jq

Create a note
curl -s -X POST "${BASE}/notes" \
  -H "Content-Type: application/json" \
  -d '{"title":"New Note","content":"Hello world"}'

Get a note
curl -s "${BASE}/notes/1"

Update a note
curl -s -X PUT "${BASE}/notes/1" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title","content":"Updated body"}'

Delete a note
curl -i -X DELETE "${BASE}/notes/1"

Expected Status Codes
- POST /notes: 201 Created
- GET /notes/{id}: 200 OK (404 if not found)
- PUT /notes/{id}: 200 OK (404 if not found)
- DELETE /notes/{id}: 204 No Content (404 if not found)