# Proposal: Full System Integration — EduTrack AI Checklist

## Why

The EduTrack AI frontend currently runs entirely on mock/demo data. The Xano backend has authentication,
subjects CRUD, and table schemas in place, but zero integration exists with the Streamlit UI.
The academic tasks table has no API endpoints, the pages for Disciplines and Tasks are placeholders,
and the Profile page is empty. This change wires every checklist item to the real backend.

## What Changes

### Backend (XanoScript)
1. **`subjects` table** — add `text? professor` and `text? schedule` fields so the UI can store
   professor name and class day/time alongside the subject name.
2. **`apis/academic_tasks/`** — new API group with full CRUD:
   - `POST  /academic_tasks`             — create task linked to subject + user
   - `GET   /academic_tasks/list`        — list user's tasks (filter by subject, status)
   - `GET   /academic_tasks/get`         — single task by id
   - `PATCH /academic_tasks/update`      — edit task fields
   - `PATCH /academic_tasks/complete`    — mark task as completed
   - `DELETE /academic_tasks/delete`     — delete task

### Frontend (Streamlit Python)
3. **`.streamlit/secrets.toml`** — store `XANO_BASE_URL` so it's configurable.
4. **`utils/xano_client.py`** — thin HTTP wrapper: attaches `Authorization: Bearer <token>` from
   `st.session_state`, raises friendly errors on 4xx/5xx.
5. **`app.py`** — auth gate: show login/signup when unauthenticated; dashboard with real Xano data when
   authenticated. Token stored in `st.session_state`.
6. **`pages/1_📚_Disciplinas.py`** — full CRUD: list from Xano, create (with professor + schedule),
   edit, delete (with confirmation), search by name, filter by overdue tasks.
7. **`pages/2_📝_Tarefas.py`** — full CRUD: list from Xano grouped by subject, create linked to a
   subject, edit, mark complete, delete, filter by status, visual overdue badge.
8. **`pages/3_👤_Perfil.py`** — view and edit name/email via `PATCH /user/edit_profile`;
   logout clears session.

## Impact

- All checklist items (auth, disciplines, tasks, dashboard, profile) become functional.
- No existing .xs file is modified except `tables/subjects.xs` (two new nullable fields).
- The `run_search` subprocess call in app.py is replaced with a direct call to the Xano
  `GET /subjects/search` endpoint (no more local subprocess).
- Demo data (DEMO_SUBJECTS, DEMO_TASKS) is removed from app.py entirely.
