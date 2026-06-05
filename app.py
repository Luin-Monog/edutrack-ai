import streamlit as st
from datetime import datetime, timezone

import utils.xano_client as api
from utils.theme import UNDERDARK_CSS, SPORE_DIVIDER

st.set_page_config(
    page_title="EduTrack AI",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(UNDERDARK_CSS, unsafe_allow_html=True)


# ── Auth helpers ───────────────────────────────────────────────────────────────

def do_login(email: str, password: str) -> None:
    try:
        data = api.auth_login(email, password)
        st.session_state["token"]   = data["authToken"]
        st.session_state["user_id"] = data.get("user_id")
        st.rerun()
    except Exception as e:
        st.error(f"Credenciais inválidas: {e}")


def do_signup(name: str, email: str, password: str) -> None:
    try:
        data = api.auth_signup(name, email, password)
        st.session_state["token"]   = data["authToken"]
        st.session_state["user_id"] = data.get("user_id")
        st.rerun()
    except Exception as e:
        st.error(f"Erro ao criar conta: {e}")


# ── Login / Signup screen ──────────────────────────────────────────────────────

def show_auth_screen() -> None:
    st.markdown("""
    <style>
    [data-testid="stSidebar"]        { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; padding: 3rem 1rem 1.5rem;">
        <div style="font-size:4rem; margin-bottom:.5rem; filter: drop-shadow(0 0 20px #8b5cf6);">🍄</div>
        <h1 style="font-family:'Cinzel',serif; font-size:2.8rem; color:#c084fc;
                   text-shadow: 0 0 30px rgba(139,92,246,0.8), 0 0 60px rgba(34,211,238,0.3);
                   letter-spacing:4px; margin:0;">EduTrack AI</h1>
        <p style="color:#a78bfa; font-size:1rem; margin-top:.5rem; letter-spacing:1px;">
            ✦ Seu reino acadêmico nas profundezas ✦
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)

    _, col_form, _ = st.columns([1, 2, 1])
    with col_form:
        tab_login, tab_signup = st.tabs(["🔮 Entrar", "🌱 Criar Conta"])

        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("form_login"):
                email    = st.text_input("E-mail",    placeholder="seu@email.com")
                password = st.text_input("Senha",     type="password")
                submitted = st.form_submit_button("⚡ Entrar no Reino", use_container_width=True, type="primary")
            if submitted:
                if email and password:
                    do_login(email, password)
                else:
                    st.warning("Preencha e-mail e senha.")

            with st.expander("🔑 Esqueci minha senha"):
                st.markdown("**Passo 1 — Solicitar código**")
                col_re, col_rb = st.columns([3, 1])
                with col_re:
                    reset_email = st.text_input("E-mail da conta", key="reset_email")
                with col_rb:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Enviar", use_container_width=True):
                        if reset_email.strip():
                            try:
                                api.auth_request_reset(reset_email.strip())
                                st.success("Código enviado!")
                            except Exception as e:
                                st.error(f"Erro: {e}")
                        else:
                            st.warning("Digite seu e-mail.")
                st.markdown("---")
                st.markdown("**Passo 2 — Criar nova senha**")
                with st.form("form_reset_password"):
                    r_email   = st.text_input("E-mail",         key="r_email")
                    r_code    = st.text_input("Código do e-mail")
                    r_pass    = st.text_input("Nova senha (mín. 8 car.)", type="password")
                    r_confirm = st.text_input("Confirmar senha",          type="password")
                    reset_submitted = st.form_submit_button("Redefinir senha", type="primary", use_container_width=True)
                if reset_submitted:
                    if not all([r_email, r_code, r_pass, r_confirm]):
                        st.warning("Preencha todos os campos.")
                    elif len(r_pass) < 8:
                        st.warning("Mínimo 8 caracteres.")
                    elif r_pass != r_confirm:
                        st.error("As senhas não coincidem.")
                    else:
                        try:
                            login_data = api.auth_magic_link_login(r_code.strip(), r_email.strip())
                            api.auth_update_password(r_pass, r_confirm, login_data["authToken"])
                            st.success("Senha redefinida! Faça login.")
                        except Exception as e:
                            st.error(f"Erro: {e}")

        with tab_signup:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("form_signup"):
                name       = st.text_input("Nome completo")
                email_s    = st.text_input("E-mail",           key="signup_email")
                password_s = st.text_input("Senha (mín. 8 car.)", type="password", key="signup_pass")
                submitted_s = st.form_submit_button("🌱 Criar minha conta", use_container_width=True, type="primary")
            if submitted_s:
                if name and email_s and password_s:
                    do_signup(name, email_s, password_s)
                else:
                    st.warning("Preencha todos os campos.")

    st.markdown("""
    <p style="text-align:center; color:#3b1f72; font-size:.8rem; margin-top:3rem;">
        EduTrack AI · Reino Fungi &amp; Underdark · Innovation Lab
    </p>
    """, unsafe_allow_html=True)


# ── Dashboard page content ─────────────────────────────────────────────────────

def show_dashboard() -> None:
    st.markdown("""
    <h1 style="display:flex; align-items:center; gap:.75rem;">
        <span style="font-size:2rem; filter:drop-shadow(0 0 12px #22d3ee);">🏠</span> Dashboard
    </h1>
    """, unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:#a78bfa'>Bem-vindo de volta, "
        f"<b style='color:#c084fc'>{st.session_state.get('user_name','Aventureiro')}</b>"
        f" — seu reino aguarda.</p>",
        unsafe_allow_html=True,
    )

    with st.spinner("Carregando dados do reino…"):
        try:    subjects = api.subjects_list()
        except: subjects = []
        try:    tasks = api.tasks_list()
        except: tasks = []

    active_subjects = [s for s in subjects if not s.get("archived", False)]
    today = datetime.now(tz=timezone.utc)

    def _due(t):
        raw = t.get("due_date")
        if raw is None: return None
        try:    return datetime.fromtimestamp(int(raw)/1000, tz=timezone.utc)
        except:
            try:
                from dateutil import parser as dp
                return dp.parse(str(raw)).replace(tzinfo=timezone.utc)
            except: return None

    pending_tasks   = [t for t in tasks if t.get("status") != "completed"]
    overdue_tasks   = [t for t in pending_tasks if (d := _due(t)) and d < today]
    completed_tasks = [t for t in tasks if t.get("status") == "completed"]
    progress_pct    = int(len(completed_tasks) / len(tasks) * 100) if tasks else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🍄 Disciplinas Ativas", len(active_subjects))
    c2.metric("⏰ Atrasadas", len(overdue_tasks),
              delta=f"-{len(overdue_tasks)}" if overdue_tasks else None, delta_color="inverse")
    c3.metric("📝 Pendentes", len(pending_tasks))
    c4.metric("✨ Progresso",  f"{progress_pct}%")

    st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 🔥 Disciplinas com Tarefas Atrasadas")
        overdue_by_subj: dict = {}
        for t in overdue_tasks:
            sid = t.get("subject_id")
            if sid: overdue_by_subj[sid] = overdue_by_subj.get(sid, 0) + 1

        behind = [s for s in active_subjects if s.get("id") in overdue_by_subj]
        if behind:
            for s in behind:
                n = overdue_by_subj[s["id"]]
                st.markdown(
                    f'<div class="fungi-card"><h4>{s["name"]} '
                    f'<span class="badge-overdue">⚠ {n} atrasada{"s" if n>1 else ""}</span></h4>'
                    f'<p>{"📅 "+s.get("semester","") if s.get("semester") else ""}'
                    f'{"  ·  👤 "+s.get("professor","") if s.get("professor") else ""}</p></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.success("✨ Nenhuma disciplina com tarefas atrasadas!")

    with col_right:
        st.markdown("### 🌙 Próximas Tarefas")
        subj_map = {s["id"]: s["name"] for s in subjects}
        upcoming = sorted(
            [t for t in pending_tasks if (d := _due(t)) and d >= today],
            key=lambda t: _due(t),
        )[:5]
        if upcoming:
            for t in upcoming:
                d = _due(t)
                due_str   = d.strftime("%d/%m/%Y") if d else "—"
                subj_name = subj_map.get(t.get("subject_id"), "—")
                prio      = t.get("priority", "media")
                prio_badge = f'<span class="badge-{prio}">{"🔴" if prio=="alta" else "🟠" if prio=="media" else "🟢"}</span>'
                st.markdown(
                    f'<div class="fungi-card"><h4>{prio_badge} {t["title"]}'
                    f' <span class="badge-pending">📅 {due_str}</span></h4>'
                    f'<p>📚 {subj_name}</p></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("🌿 Nenhuma tarefa próxima.")

    if tasks and active_subjects:
        st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)
        st.markdown("### 🌿 Progresso por Disciplina")
        cols = st.columns(min(len(active_subjects), 3))
        for i, s in enumerate(active_subjects):
            s_tasks = [t for t in tasks if t.get("subject_id") == s["id"]]
            s_done  = [t for t in s_tasks if t.get("status") == "completed"]
            pct = int(len(s_done) / len(s_tasks) * 100) if s_tasks else 0
            with cols[i % 3]:
                st.markdown(f"**{s['name']}**")
                st.progress(pct / 100)
                st.caption(f"{len(s_done)}/{len(s_tasks)} concluídas · {pct}%")

    if not subjects:
        st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; padding:2rem; background:linear-gradient(135deg,#1e1438,#120d24);
                    border:1px solid #3b1f72; border-radius:16px;">
            <div style="font-size:3rem; filter:drop-shadow(0 0 16px #8b5cf6);">🍄</div>
            <h2 style="color:#c084fc; font-family:'Cinzel',serif;">Bem-vindo ao Reino!</h2>
            <p style="color:#a78bfa;">Crie sua primeira disciplina para começar.</p>
        </div>
        """, unsafe_allow_html=True)


# ── Entry point ────────────────────────────────────────────────────────────────

if "token" not in st.session_state:
    show_auth_screen()
    st.stop()

# Load user name once per session
if "user_name" not in st.session_state:
    try:
        me = api.auth_me()
        st.session_state["user_name"] = me.get("name", "Aventureiro")
    except Exception:
        st.session_state["user_name"] = "Aventureiro"

# ── Sidebar (above nav links) ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:.5rem 0 .75rem;">
        <div style="font-size:2.5rem; filter:drop-shadow(0 0 14px #8b5cf6);">🍄</div>
        <div style="font-family:'Cinzel',serif; color:#c084fc; font-size:.85rem; letter-spacing:2px;">EduTrack AI</div>
    </div>
    """, unsafe_allow_html=True)

# ── Navigation (renders nav links in sidebar automatically) ────────────────────
pg = st.navigation([
    st.Page(show_dashboard,                    title="Dashboard",  icon="🏠", default=True),
    st.Page("pages/1_📚_Disciplinas.py",       title="Disciplinas", icon="📚"),
    st.Page("pages/2_📝_Tarefas.py",           title="Tarefas",    icon="📝"),
    st.Page("pages/3_👤_Perfil.py",            title="Perfil",     icon="👤"),
    st.Page("pages/4_📊_Relatorios.py",        title="Relatórios", icon="📊"),
])

# ── Sidebar (below nav links) ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown(
        f"<div style='color:#a78bfa; font-size:.85rem; padding:.25rem 0'>👤 {st.session_state.get('user_name','Aventureiro')}</div>",
        unsafe_allow_html=True,
    )
    st.caption("Innovation Lab · v0.4.0")
    st.markdown("---")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.clear()
        st.rerun()

pg.run()
