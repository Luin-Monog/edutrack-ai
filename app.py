import streamlit as st
from datetime import datetime, timezone

import utils.xano_client as api

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduTrack AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%); }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

.subject-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155; border-radius: 12px;
    padding: 1rem 1.25rem; margin-bottom: .75rem;
}
.subject-card h4 { color: #e2e8f0; margin: 0 0 .3rem; font-size: 1rem; }
.subject-card p  { color: #94a3b8; margin: 0; font-size: .85rem; }
.tag-overdue { background:#7f1d1d; color:#fca5a5; border-radius:6px; padding:2px 8px; font-size:.75rem; font-weight:600; }
.tag-ok      { background:#14532d; color:#86efac; border-radius:6px; padding:2px 8px; font-size:.75rem; font-weight:600; }
.tag-pending { background:#1e3a5f; color:#93c5fd; border-radius:6px; padding:2px 8px; font-size:.75rem; font-weight:600; }

[data-testid="metric-container"] {
    background:#1e293b; border-radius:10px;
    padding:.75rem 1rem; border:1px solid #334155;
}
.auth-box {
    max-width: 420px; margin: 4rem auto 0;
    background: #1e293b; border: 1px solid #334155;
    border-radius: 16px; padding: 2rem;
}
</style>
""", unsafe_allow_html=True)


# ── Auth helpers ───────────────────────────────────────────────────────────────

def do_login(email: str, password: str) -> None:
    try:
        data = api.auth_login(email, password)
        st.session_state["token"] = data["authToken"]
        st.session_state["user_id"] = data.get("user_id")
        st.rerun()
    except Exception as e:
        st.error(f"Erro ao entrar: {e}")


def do_signup(name: str, email: str, password: str) -> None:
    try:
        data = api.auth_signup(name, email, password)
        st.session_state["token"] = data["authToken"]
        st.session_state["user_id"] = data.get("user_id")
        st.rerun()
    except Exception as e:
        st.error(f"Erro ao criar conta: {e}")


# ── Login / Signup screen ──────────────────────────────────────────────────────

def show_auth_screen() -> None:
    st.markdown(
        "<div style='text-align:center;margin-top:2rem'>"
        "<h1>🎓 EduTrack AI</h1>"
        "<p style='color:#94a3b8'>Seu assistente acadêmico inteligente</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    tab_login, tab_signup = st.tabs(["Entrar", "Criar Conta"])

    with tab_login:
        with st.form("form_login"):
            st.subheader("Bem-vindo de volta!")
            email = st.text_input("E-mail", placeholder="seu@email.com")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar", use_container_width=True, type="primary")
        if submitted:
            if email and password:
                do_login(email, password)
            else:
                st.warning("Preencha e-mail e senha.")

    with tab_signup:
        with st.form("form_signup"):
            st.subheader("Crie sua conta")
            name = st.text_input("Nome completo")
            email_s = st.text_input("E-mail", placeholder="seu@email.com", key="signup_email")
            password_s = st.text_input("Senha", type="password", key="signup_pass")
            submitted_s = st.form_submit_button("Criar Conta", use_container_width=True, type="primary")
        if submitted_s:
            if name and email_s and password_s:
                do_signup(name, email_s, password_s)
            else:
                st.warning("Preencha todos os campos.")


# ── Dashboard ──────────────────────────────────────────────────────────────────

def show_dashboard() -> None:
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎓 EduTrack AI")
        st.markdown("---")
        user_name = st.session_state.get("user_name", "Usuário")
        st.markdown(f"👤 **{user_name}**")
        st.markdown("---")
        st.caption("Innovation Lab · v0.3.0")
        st.markdown("---")
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.title("🏠 Dashboard")
    st.markdown("Bem-vindo ao **EduTrack AI** — seu assistente acadêmico inteligente.")

    # Load data
    with st.spinner("Carregando dados…"):
        try:
            subjects = api.subjects_list()
        except Exception:
            subjects = []
        try:
            tasks = api.tasks_list()
        except Exception:
            tasks = []

    today = datetime.now(tz=timezone.utc)

    def _due(t: dict):
        raw = t.get("due_date")
        if raw is None:
            return None
        try:
            return datetime.fromtimestamp(int(raw) / 1000, tz=timezone.utc)
        except Exception:
            try:
                from dateutil import parser as dp
                return dp.parse(str(raw)).replace(tzinfo=timezone.utc)
            except Exception:
                return None

    pending_tasks = [t for t in tasks if t.get("status") != "completed"]
    overdue_tasks = [t for t in pending_tasks if (d := _due(t)) and d < today]
    completed_tasks = [t for t in tasks if t.get("status") == "completed"]
    progress_pct = int(len(completed_tasks) / len(tasks) * 100) if tasks else 0

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Disciplinas", len(subjects))
    col2.metric(
        "⏰ Tarefas Atrasadas",
        len(overdue_tasks),
        delta=f"-{len(overdue_tasks)} em atraso" if overdue_tasks else None,
        delta_color="inverse",
    )
    col3.metric("📝 Tarefas Pendentes", len(pending_tasks))
    col4.metric("✅ Progresso Geral", f"{progress_pct}%")

    st.markdown("---")

    # Subjects with overdue tasks
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Disciplinas com Tarefas Atrasadas")
        overdue_by_subject: dict[int, int] = {}
        for t in overdue_tasks:
            sid = t.get("subject_id")
            if sid:
                overdue_by_subject[sid] = overdue_by_subject.get(sid, 0) + 1

        subjects_with_overdue = [s for s in subjects if s.get("id") in overdue_by_subject]

        if subjects_with_overdue:
            for s in subjects_with_overdue:
                n = overdue_by_subject[s["id"]]
                st.markdown(
                    f'<div class="subject-card"><h4>{s["name"]} '
                    f'<span class="tag-overdue">⚠ {n} atrasada{"s" if n > 1 else ""}</span></h4>'
                    f'<p>{s.get("professor","") or s.get("description","")}</p></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.success("🎉 Nenhuma disciplina com tarefas atrasadas!")

    with col_right:
        st.subheader("Próximas Tarefas")
        upcoming = sorted(
            [t for t in pending_tasks if _due(t) and _due(t) >= today],
            key=lambda t: _due(t),
        )[:5]

        if upcoming:
            for t in upcoming:
                d = _due(t)
                due_str = d.strftime("%d/%m/%Y") if d else "—"
                subj = next((s["name"] for s in subjects if s.get("id") == t.get("subject_id")), "—")
                st.markdown(
                    f'<div class="subject-card">'
                    f'<h4><span class="tag-pending">📅 {due_str}</span> {t["title"]}</h4>'
                    f'<p>📚 {subj}</p></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("Nenhuma tarefa próxima.")

    # Welcome for new users
    if not subjects and not tasks:
        st.markdown("---")
        st.info(
            "👋 Parece que você ainda não tem disciplinas ou tarefas cadastradas. "
            "Acesse **Disciplinas** no menu lateral para começar!"
        )


# ── Entry point ────────────────────────────────────────────────────────────────

if "token" not in st.session_state:
    show_auth_screen()
else:
    # Try to load user name once per session
    if "user_name" not in st.session_state:
        try:
            me = api.auth_me()
            st.session_state["user_name"] = me.get("name", "Usuário")
        except Exception:
            st.session_state["user_name"] = "Usuário"
    show_dashboard()
