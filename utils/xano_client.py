"""
Thin HTTP client for the EduTrack AI Xano backend.
All functions read the auth token from st.session_state["token"].
API base URLs are read from .streamlit/secrets.toml.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests
import streamlit as st


# ── Internal helpers ──────────────────────────────────────────────────────────

def _base(group: str) -> str:
    key = f"XANO_API_{group.upper()}"
    url = st.secrets.get(key, "")
    if not url:
        raise RuntimeError(
            f"Secret '{key}' não está configurado em .streamlit/secrets.toml. "
            "Faça o push para o Xano e atualize o arquivo."
        )
    return url.rstrip("/")


def _headers(token: Optional[str] = None) -> Dict[str, str]:
    tok = token or st.session_state.get("token", "")
    h: Dict[str, str] = {}
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def _handle(resp: requests.Response) -> Any:
    if resp.ok:
        return resp.json()
    try:
        msg = resp.json().get("message", resp.text)
    except Exception:
        msg = resp.text
    raise requests.HTTPError(msg, response=resp)


# ── Authentication ─────────────────────────────────────────────────────────────

def auth_login(email: str, password: str) -> Dict:
    r = requests.post(
        f"{_base('AUTH')}/auth/login",
        json={"email": email, "password": password},
        timeout=15,
    )
    return _handle(r)


def auth_signup(name: str, email: str, password: str) -> Dict:
    r = requests.post(
        f"{_base('AUTH')}/auth/signup",
        json={"name": name, "email": email, "password": password},
        timeout=15,
    )
    return _handle(r)


def auth_me() -> Dict:
    r = requests.get(
        f"{_base('AUTH')}/auth/me",
        headers=_headers(),
        timeout=15,
    )
    return _handle(r)


# ── Password reset ────────────────────────────────────────────────────────────

def auth_request_reset(email: str) -> Dict:
    r = requests.get(
        f"{_base('AUTH')}/reset/request-reset-link",
        params={"email": email},
        timeout=15,
    )
    return _handle(r)


def auth_magic_link_login(magic_token: str, email: str) -> Dict:
    r = requests.post(
        f"{_base('AUTH')}/reset/magic-link-login",
        json={"magic_token": magic_token, "email": email},
        timeout=15,
    )
    return _handle(r)


def auth_update_password(password: str, confirm_password: str, temp_token: str) -> Dict:
    r = requests.post(
        f"{_base('AUTH')}/reset/update_password",
        json={"password": password, "confirm_password": confirm_password},
        headers={"Authorization": f"Bearer {temp_token}"},
        timeout=15,
    )
    return _handle(r)


# ── Profile ────────────────────────────────────────────────────────────────────

def user_edit_profile(name: Optional[str] = None, email: Optional[str] = None) -> Dict:
    payload: Dict[str, str] = {}
    if name:
        payload["name"] = name
    if email:
        payload["email"] = email
    r = requests.patch(
        f"{_base('MEMBERS')}/user/edit_profile",
        json=payload,
        headers=_headers(),
        timeout=15,
    )
    return _handle(r)


# ── Subjects ───────────────────────────────────────────────────────────────────

def subjects_list() -> List[Dict]:
    r = requests.get(
        f"{_base('SUBJECTS')}/subjects/list",
        headers=_headers(),
        timeout=15,
    )
    return _handle(r)


def subjects_create(
    name: str,
    description: Optional[str] = None,
    professor: Optional[str] = None,
    schedule: Optional[str] = None,
    semester: Optional[str] = None,
    visibility: str = "private",
) -> Dict:
    r = requests.post(
        f"{_base('SUBJECTS')}/subjects/create",
        json={
            "name": name,
            "description": description,
            "professor": professor,
            "schedule": schedule,
            "semester": semester,
            "visibility": visibility,
        },
        headers=_headers(),
        timeout=15,
    )
    return _handle(r)


def subjects_update(subject_id: int, **kwargs) -> Dict:
    # Only send fields that have a real value; omit None so Xano won't complain
    # about missing optional params.
    payload = {k: v for k, v in kwargs.items() if v is not None}
    r = requests.patch(
        f"{_base('SUBJECTS')}/subjects/update",
        json={"subject_id": subject_id, **payload},
        headers=_headers(),
        timeout=15,
    )
    return _handle(r)


def subjects_delete(subject_id: int) -> Dict:
    r = requests.delete(
        f"{_base('SUBJECTS')}/subjects/delete",
        json={"subject_id": subject_id},
        headers=_headers(),
        timeout=15,
    )
    return _handle(r)


def subjects_search(query: str = "", include_overdue: bool = False) -> List[Dict]:
    r = requests.get(
        f"{_base('SUBJECTS')}/subjects/search",
        params={"query": query, "include_overdue": str(include_overdue).lower()},
        headers=_headers(),
        timeout=25,
    )
    return _handle(r)


# ── Academic Tasks ─────────────────────────────────────────────────────────────

def tasks_list() -> List[Dict]:
    try:
        r = requests.get(
            f"{_base('TASKS')}/academic_tasks/list",
            params={"subject_id": 0, "status": "all"},
            headers=_headers(),
            timeout=15,
        )
        return _handle(r)
    except RuntimeError:
        return []


def tasks_create(
    title: str,
    due_date: str,
    subject_id: int,
    description: Optional[str] = None,
    status: str = "pending",
    priority: str = "media",
) -> Dict:
    r = requests.post(
        f"{_base('TASKS')}/academic_tasks/create",
        json={
            "title": title,
            "due_date": due_date,
            "subject_id": subject_id,
            "description": description,
            "status": status,
            "priority": priority,
        },
        headers=_headers(),
        timeout=15,
    )
    return _handle(r)


def tasks_update(task_id: int, title: Optional[str] = None, **kwargs) -> Dict:
    # Xano requires title in updates even if we're only changing other fields
    payload = {k: v for k, v in {**kwargs, "title": title}.items() if v is not None}
    r = requests.patch(
        f"{_base('TASKS')}/academic_tasks/update",
        json={"task_id": task_id, **payload},
        headers=_headers(),
        timeout=15,
    )
    return _handle(r)


def tasks_complete(task_id: int) -> Dict:
    r = requests.patch(
        f"{_base('TASKS')}/academic_tasks/complete",
        json={"task_id": task_id, "status": "completed"},
        headers=_headers(),
        timeout=15,
    )
    return _handle(r)


def tasks_delete(task_id: int) -> Dict:
    r = requests.delete(
        f"{_base('TASKS')}/academic_tasks/delete",
        json={"task_id": task_id},
        headers=_headers(),
        timeout=15,
    )
    return _handle(r)


# ── Date utilities ─────────────────────────────────────────────────────────────

def ms_to_date_str(ms: Any) -> str:
    """Convert Xano millisecond timestamp to YYYY-MM-DD string."""
    if ms is None:
        return ""
    try:
        from datetime import datetime, timezone
        return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
    except Exception:
        return str(ms)
