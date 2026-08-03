# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

Minimal scaffolding is in place: a `.venv` (Python 3.12), `requirements.txt` (fastapi, uvicorn[standard]),
and `app/main.py` with a single `/health` endpoint. No Todo domain code, database layer, or ORM has been
added yet.

## Common commands

```powershell
# activate the venv (or call .\.venv\Scripts\python.exe / pip.exe directly)
.\.venv\Scripts\Activate.ps1

# install/update dependencies
pip install -r requirements.txt

# run the dev server (reload enabled)
uvicorn app.main:app --reload --port 8000
```

## Assignment requirements (from README.md)

Build a Todo management REST API with the following constraints:

* **Language/framework**: Python 3.12+ with FastAPI
* **Storage**: SQLite (required)
* **Version control**: Git / GitHub
* ORM choice, package manager, and project structure are free choices — none are mandated.
* A Todo must include at minimum a title and a completed/done flag. Optional extras (description, due
  date, priority, tags, search, pagination, auth) may be added but are not required.
* CRUD is required: create, read, update, delete.
* API route design and response shapes are up to the implementer, but must use appropriate HTTP methods
  and status codes, and must handle invalid input and not-found cases explicitly.
* The final `README.md` must document: how to run the project, technologies used, the list of API
  endpoints, and which features were implemented (this replaces the current placeholder README).

## Getting started on this repo

Since no scaffolding exists, the first implementation pass will need to establish (and should pick
sensible, minimal choices for) a package manager (e.g. `pip`/`venv`, `poetry`, or `uv`), project layout,
and an ORM or raw `sqlite3`/`aiosqlite` access layer — there is no existing convention to follow yet.
