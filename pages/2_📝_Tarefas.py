import streamlit as st
from datetime import datetime, timezone, date

import utils.xano_client as api
from utils.theme import UNDERDARK_CSS, SPORE_DIVIDER, PRIORITY_BADGE, STATUS_BADGE

st.set_page_config(page_title="Tarefas", page_icon="📝", layout="wide")
st.markdown(UNDERDARK_CSS, unsafe_allow_html=True)

if "token" not in st.session_state:
    st.warning("Faça login primeiro.")
    st.page_link("app.py", label="Ir para o Login", icon="🔑")
    st.stop()

with st.sidebar:
    st.markdown(f"<div style='color:#a78bfa; font-size:.85rem;'>👤 {st.session_state.get('user_name','Usuário')}</div>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.markdown("# 📝 Minhas Tarefas")
st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────

def load_data():
    try:
        st.session_state["tasks_cache"]    = api.tasks_list()
    except Exception as e:
        st.error(f"Erro ao carregar tarefas: {e}")
        st.session_state["tasks_cache"] = []
    try:
        st.session_state["subjects_cache"] = api.subjects_list()
    except Exception:
        st.session_state.setdefault("subjects_cache", [])


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


STATUS_LABELS = {"pending": "Pendente", "in_progress": "Em andamento", "completed": "Concluída"}
PRIORITY_LABELS = {"baixa": "Baixa", "media": "Média", "alta": "Alta"}

if "tasks_cache" not in st.session_state:
    load_data()

tasks: list    = st.session_state.get("tasks_cache", [])
subjects: list = st.session_state.get("subjects_cache", [])
subjects_map   = {s["id"]: s for s in subjects}

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_lista, tab_nova = st.tabs(["📋 Minhas Tarefas", "➕ Nova Tarefa"])

# ════════════════════════════════════════════════════════════════════════════
# TAB: LISTAR
# ════════════════════════════════════════════════════════════════════════════
with tab_lista:
    col_r, col_fs, col_fp = st.columns([1, 2, 2])
    with col_r:
        if st.button("🔄 Atualizar", use_container_width=True):
            load_data()
            st.rerun()
    with col_fs:
        status_filter = st.selectbox(
            "Status", ["Todas", "Pendente", "Em andamento", "Concluída"],
            label_visibility="collapsed",
        )
    with col_fp:
        prio_filter = st.selectbox(
            "Prioridade", ["Todas", "Alta", "Média", "Baixa"],
            label_visibility="collapsed",
        )

    tasks = st.session_state.get("tasks_cache", [])

    status_map = {"Pendente": "pending", "Em andamento": "in_progress", "Concluída": "completed"}
    prio_map   = {"Alta": "alta", "Média": "media", "Baixa": "baixa"}

    filtered = tasks
    if status_filter != "Todas":
        filtered = [t for t in filtered if t.get("status") == status_map[status_filter]]
    if prio_filter != "Todas":
        filtered = [t for t in filtered if t.get("priority") == prio_map[prio_filter]]

    if not filtered:
        st.info("Nenhuma tarefa encontrada para os filtros selecionados.")
    else:
        by_subject: dict[int, list] = {}
        for t in filtered:
            sid = t.get("subject_id", 0)
            by_subject.setdefault(sid, []).append(t)

        for sid, group in by_subject.items():
            subj = subjects_map.get(sid, {})
            st.markdown(f"### 📚 {subj.get('name', 'Sem disciplina')}")

            for t in sorted(group, key=lambda x: _due_dt(x) or datetime.max.replace(tzinfo=timezone.utc)):
                overdue = _is_overdue(t)
                prio    = t.get("priority", "media")
                status  = t.get("status", "pending")

                overdue_tag = ' <span class="badge-overdue">🔴 Atrasada</span>' if overdue else ""
                prio_html   = PRIORITY_BADGE.get(prio, "")
                status_html = STATUS_BADGE.get(status, "")

                with st.expander(
                    f"{prio_html} {t['title']}  ·  {_due_str(t)}{overdue_tag}",
                    expanded=overdue,
                ):
                    col_info, col_act = st.columns([3, 1])

                    with col_info:
                        st.markdown(
                            f"{status_html} &nbsp; {prio_html}",
                            unsafe_allow_html=True,
                        )
                        st.markdown(f"**Prazo:** {_due_str(t)}")
                        if t.get("description"):
                            st.markdown(f"**Descrição:** {t['description']}")

                    with col_act:
                        if status != "completed":
                            if st.button("✅ Concluir", key=f"done_{t['id']}"):
                                try:
                                    api.tasks_complete(t["id"])
                                    load_data()
                                    st.rerun()
                                except Exception as e:
                                    st.error(str(e))

                        with st.popover("✏️ Editar"):
                            with st.form(f"edit_task_{t['id']}"):
                                e_title = st.text_input("Título", value=t.get("title", ""))
                                e_desc  = st.text_area("Descrição", value=t.get("description") or "", height=60)
                                cur_due = _due_dt(t)
                                e_due   = st.date_input("Prazo", value=cur_due.date() if cur_due else date.today(), format="DD/MM/YYYY")
                                e_status = st.selectbox("Status", list(STATUS_LABELS.keys()),
                                                        format_func=lambda k: STATUS_LABELS[k],
                                                        index=list(STATUS_LABELS.keys()).index(status))
                                e_prio  = st.selectbox("Prioridade", list(PRIORITY_LABELS.keys()),
                                                       format_func=lambda k: PRIORITY_LABELS[k],
                                                       index=list(PRIORITY_LABELS.keys()).index(prio))
                                save_e = st.form_submit_button("Salvar", type="primary")
                            if save_e:
                                try:
                                    api.tasks_update(t["id"],
                                                     title=e_title or None,
                                                     description=e_desc or None,
                                                     due_date=e_due.strftime("%Y-%m-%d"),
                                                     status=e_status, priority=e_prio)
                                    load_data()
                                    st.rerun()
                                except Exception as e:
                                    st.error(str(e))

                        with st.popover("🗑️ Excluir"):
                            st.warning(f"Excluir **{t['title']}**?")
                            if st.button("Confirmar", key=f"deltask_{t['id']}", type="primary"):
                                try:
                                    api.tasks_delete(t["id"])
                                    load_data()
                                    st.rerun()
                                except Exception as e:
                                    st.error(str(e))

# ════════════════════════════════════════════════════════════════════════════
# TAB: NOVA TAREFA
# ════════════════════════════════════════════════════════════════════════════
with tab_nova:
    st.subheader("Cadastrar Nova Tarefa")
    active_subjects = [s for s in subjects if not s.get("archived", False)]

    if not active_subjects:
        st.warning("Você precisa ter pelo menos uma disciplina ativa antes de criar tarefas.")
        st.page_link("pages/1_📚_Disciplinas.py", label="Ir para Disciplinas", icon="📚")
    else:
        subj_opts = {s["name"]: s["id"] for s in active_subjects}

        if "task_form_key" not in st.session_state:
            st.session_state["task_form_key"] = 0

        with st.form(f"form_create_task_{st.session_state['task_form_key']}"):
            title       = st.text_input("Título da Tarefa *", placeholder="Ex: Lista 3 – Derivadas")
            description = st.text_area("Descrição (opcional)", height=80)
            col_d, col_p = st.columns(2)
            with col_d:
                due_date = st.date_input("Prazo *", value=date.today(), format="DD/MM/YYYY")
            with col_p:
                prio_new = st.selectbox("Prioridade", list(PRIORITY_LABELS.keys()),
                                        format_func=lambda k: PRIORITY_LABELS[k],
                                        index=1)
            subj_name  = st.selectbox("Disciplina *", options=list(subj_opts.keys()))
            status_new = st.selectbox("Status inicial", list(STATUS_LABELS.keys()),
                                      format_func=lambda k: STATUS_LABELS[k])
            submitted  = st.form_submit_button("✨ Salvar Tarefa", type="primary", use_container_width=True)

        if submitted:
            if not title.strip():
                st.warning("O título é obrigatório.")
            else:
                try:
                    api.tasks_create(
                        title=title.strip(),
                        due_date=due_date.strftime("%Y-%m-%d"),
                        subject_id=subj_opts[subj_name],
                        description=description.strip() or None,
                        status=status_new,
                        priority=prio_new,
                    )
                    st.success(f"✨ Tarefa **{title}** criada!")
                    load_data()
                    st.session_state["task_form_key"] += 1
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao criar tarefa: {e}")
