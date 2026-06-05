import streamlit as st
from datetime import datetime, timezone, date

import utils.xano_client as api

st.set_page_config(page_title="Tarefas", page_icon="📝", layout="wide")

# ── Auth guard ─────────────────────────────────────────────────────────────────
if "token" not in st.session_state:
    st.warning("Faça login primeiro.")
    st.page_link("app.py", label="Ir para o Login", icon="🔑")
    st.stop()

# ── Sidebar logout ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"👤 **{st.session_state.get('user_name', 'Usuário')}**")
    st.markdown("---")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.title("📝 Minhas Tarefas")

# ── Helpers ────────────────────────────────────────────────────────────────────

def load_data():
    try:
        st.session_state["tasks_cache"] = api.tasks_list()
    except Exception as e:
        st.error(f"Erro ao carregar tarefas: {e}")
        st.session_state["tasks_cache"] = []
    try:
        st.session_state["subjects_cache"] = api.subjects_list()
    except Exception as e:
        st.session_state["subjects_cache"] = []


def _due_dt(task: dict):
    raw = task.get("due_date")
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


def _due_str(task: dict) -> str:
    d = _due_dt(task)
    return d.strftime("%d/%m/%Y") if d else "—"


def _is_overdue(task: dict) -> bool:
    if task.get("status") == "completed":
        return False
    d = _due_dt(task)
    return d is not None and d < datetime.now(tz=timezone.utc)


STATUS_LABELS = {
    "pending": "Pendente",
    "in_progress": "Em andamento",
    "completed": "Concluída",
}

STATUS_ICONS = {
    "pending": "🟡",
    "in_progress": "🔵",
    "completed": "✅",
}


# ── Initial load ───────────────────────────────────────────────────────────────
if "tasks_cache" not in st.session_state:
    load_data()

tasks: list = st.session_state.get("tasks_cache", [])
subjects: list = st.session_state.get("subjects_cache", [])
subjects_map = {s["id"]: s for s in subjects}


# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_lista, tab_nova = st.tabs(["📋 Minhas Tarefas", "➕ Nova Tarefa"])


# ════════════════════════════════════════════════════════════════════════════════
# TAB: LISTAR
# ════════════════════════════════════════════════════════════════════════════════
with tab_lista:
    col_refresh, col_filter, _ = st.columns([1, 2, 3])
    with col_refresh:
        if st.button("🔄 Atualizar", use_container_width=True):
            load_data()
            st.rerun()
    with col_filter:
        status_filter = st.selectbox(
            "Filtrar por status",
            options=["Todas", "Pendente", "Em andamento", "Concluída"],
            label_visibility="collapsed",
        )

    tasks = st.session_state.get("tasks_cache", [])

    status_map = {"Pendente": "pending", "Em andamento": "in_progress", "Concluída": "completed"}
    if status_filter != "Todas":
        filtered = [t for t in tasks if t.get("status") == status_map[status_filter]]
    else:
        filtered = tasks

    if not filtered:
        st.info("Nenhuma tarefa encontrada.")
    else:
        today = datetime.now(tz=timezone.utc)

        # Group by subject
        by_subject: dict[int, list] = {}
        for t in filtered:
            sid = t.get("subject_id", 0)
            by_subject.setdefault(sid, []).append(t)

        for sid, group in by_subject.items():
            subj_name = subjects_map.get(sid, {}).get("name", "Sem disciplina")
            st.markdown(f"### 📚 {subj_name}")

            for t in sorted(group, key=lambda x: _due_dt(x) or datetime.max.replace(tzinfo=timezone.utc)):
                overdue = _is_overdue(t)
                icon = STATUS_ICONS.get(t.get("status", "pending"), "🟡")
                overdue_badge = " 🔴 **Atrasada**" if overdue else ""
                label = t.get("status", "pending")
                status_label = STATUS_LABELS.get(label, label)

                with st.expander(
                    f"{icon} {t['title']}  ·  {_due_str(t)}{overdue_badge}",
                    expanded=overdue,
                ):
                    col_info, col_actions = st.columns([3, 1])

                    with col_info:
                        st.markdown(f"**Status:** {status_label}")
                        st.markdown(f"**Prazo:** {_due_str(t)}")
                        if t.get("description"):
                            st.markdown(f"**Descrição:** {t['description']}")

                    with col_actions:
                        if t.get("status") != "completed":
                            if st.button("✅ Concluir", key=f"done_{t['id']}"):
                                try:
                                    api.tasks_complete(t["id"])
                                    st.success("Marcada como concluída!")
                                    load_data()
                                    st.rerun()
                                except Exception as e:
                                    st.error(str(e))

                        with st.popover("✏️ Editar"):
                            with st.form(f"edit_task_{t['id']}"):
                                e_title = st.text_input("Título", value=t.get("title", ""))
                                e_desc = st.text_area("Descrição", value=t.get("description") or "", height=60)
                                current_due = _due_dt(t)
                                e_due = st.date_input(
                                    "Prazo",
                                    value=current_due.date() if current_due else date.today(),
                                )
                                e_status = st.selectbox(
                                    "Status",
                                    options=list(STATUS_LABELS.keys()),
                                    format_func=lambda k: STATUS_LABELS[k],
                                    index=list(STATUS_LABELS.keys()).index(t.get("status", "pending")),
                                )
                                save_e = st.form_submit_button("Salvar", type="primary")
                            if save_e:
                                try:
                                    api.tasks_update(
                                        t["id"],
                                        title=e_title or None,
                                        description=e_desc or None,
                                        due_date=e_due.strftime("%Y-%m-%d"),
                                        status=e_status,
                                    )
                                    st.success("Atualizada!")
                                    load_data()
                                    st.rerun()
                                except Exception as e:
                                    st.error(str(e))

                        with st.popover("🗑️ Excluir"):
                            st.warning(f"Excluir **{t['title']}**?")
                            if st.button("Confirmar", key=f"deltask_{t['id']}", type="primary"):
                                try:
                                    api.tasks_delete(t["id"])
                                    st.success("Excluída!")
                                    load_data()
                                    st.rerun()
                                except Exception as e:
                                    st.error(str(e))


# ════════════════════════════════════════════════════════════════════════════════
# TAB: NOVA TAREFA
# ════════════════════════════════════════════════════════════════════════════════
with tab_nova:
    st.subheader("Cadastrar Nova Tarefa")

    if not subjects:
        st.warning("Você precisa ter pelo menos uma disciplina cadastrada antes de criar tarefas.")
        st.page_link("pages/1_📚_Disciplinas.py", label="Ir para Disciplinas", icon="📚")
    else:
        subj_options = {s["name"]: s["id"] for s in subjects}

        with st.form("form_create_task"):
            title = st.text_input("Título da Tarefa *", placeholder="Ex: Lista 3 – Derivadas")
            description = st.text_area("Descrição (opcional)", height=80)
            due_date = st.date_input("Prazo *", value=date.today())
            subject_name = st.selectbox("Disciplina *", options=list(subj_options.keys()))
            status_new = st.selectbox(
                "Status inicial",
                options=list(STATUS_LABELS.keys()),
                format_func=lambda k: STATUS_LABELS[k],
            )
            submitted = st.form_submit_button("Salvar Tarefa", type="primary", use_container_width=True)

        if submitted:
            if not title.strip():
                st.warning("O título é obrigatório.")
            else:
                try:
                    api.tasks_create(
                        title=title.strip(),
                        due_date=due_date.strftime("%Y-%m-%d"),
                        subject_id=subj_options[subject_name],
                        description=description.strip() or None,
                        status=status_new,
                    )
                    st.success(f"Tarefa **{title}** criada com sucesso!")
                    load_data()
                except Exception as e:
                    st.error(f"Erro ao criar tarefa: {e}")
