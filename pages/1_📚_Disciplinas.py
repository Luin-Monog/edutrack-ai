import streamlit as st

import utils.xano_client as api
from utils.theme import UNDERDARK_CSS, SPORE_DIVIDER

st.set_page_config(page_title="Disciplinas", page_icon="📚", layout="wide")
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

st.markdown("# 📚 Gestão de Disciplinas")
st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)


def load_subjects():
    try:
        st.session_state["subjects_cache"] = api.subjects_list()
        st.session_state["tasks_cache"] = api.tasks_list()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        st.session_state.setdefault("subjects_cache", [])
        st.session_state.setdefault("tasks_cache", [])

if "subjects_cache" not in st.session_state:
    load_subjects()

subjects: list = st.session_state.get("subjects_cache", [])
tasks: list    = st.session_state.get("tasks_cache", [])

active   = [s for s in subjects if not s.get("archived", False)]
archived = [s for s in subjects if s.get("archived", False)]


def task_progress(subject_id: int):
    s_tasks = [t for t in tasks if t.get("subject_id") == subject_id]
    s_done  = [t for t in s_tasks if t.get("status") == "completed"]
    pct = int(len(s_done) / len(s_tasks) * 100) if s_tasks else 0
    return len(s_done), len(s_tasks), pct


tab_lista, tab_novo, tab_busca, tab_archive = st.tabs(
    ["📋 Disciplinas", "➕ Nova Disciplina", "🔍 Buscar", "🗄️ Arquivadas"]
)

# ════════════════════════════════════════════════════════════════════════════
# TAB: LISTAR
# ════════════════════════════════════════════════════════════════════════════
with tab_lista:
    col_r, _ = st.columns([1, 5])
    with col_r:
        if st.button("🔄 Atualizar", use_container_width=True):
            load_subjects()
            st.rerun()

    if not active:
        st.markdown("""
        <div style="text-align:center; padding:2rem; background:linear-gradient(135deg,#1e1438,#120d24);
                    border:1px solid #3b1f72; border-radius:16px;">
            <div style="font-size:2.5rem;">🌱</div>
            <p style="color:#a78bfa; margin:.5rem 0 0;">Nenhuma disciplina ativa. Crie a primeira!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for s in active:
            done, total, pct = task_progress(s["id"])
            overdue_n = sum(
                1 for t in tasks
                if t.get("subject_id") == s["id"]
                and t.get("status") != "completed"
                and t.get("due_date") is not None
                and __import__("datetime").datetime.fromtimestamp(
                    int(t["due_date"]) / 1000,
                    tz=__import__("datetime").timezone.utc
                ) < __import__("datetime").datetime.now(tz=__import__("datetime").timezone.utc)
            )

            badge_overdue = f'<span class="badge-overdue">⚠ {overdue_n} atrasada{"s" if overdue_n>1 else ""}</span>' if overdue_n else '<span class="badge-ok">✓ Em dia</span>'
            semester_tag  = f'<span style="color:#6d28d9; font-size:.8rem;">📅 {s["semester"]}</span>' if s.get("semester") else ""

            with st.expander(f"📚 {s['name']}  {semester_tag}", expanded=False):
                col_info, col_prog, col_act = st.columns([2, 2, 1])

                with col_info:
                    st.markdown(f"**Professor:** {s.get('professor') or '—'}")
                    st.markdown(f"**Horário:** {s.get('schedule') or '—'}")
                    st.markdown(f"**Semestre:** {s.get('semester') or '—'}")
                    if s.get("description"):
                        st.markdown(f"**Descrição:** {s['description']}")
                    st.markdown(badge_overdue, unsafe_allow_html=True)

                with col_prog:
                    st.markdown("**Progresso das tarefas**")
                    st.progress(pct / 100)
                    st.caption(f"{done}/{total} concluídas · {pct}%")

                with col_act:
                    with st.popover("✏️ Editar"):
                        with st.form(f"edit_{s['id']}"):
                            new_name  = st.text_input("Nome",      value=s.get("name", ""))
                            new_prof  = st.text_input("Professor", value=s.get("professor") or "")
                            new_sched = st.text_input("Horário",   value=s.get("schedule") or "")
                            new_sem   = st.text_input("Semestre",  value=s.get("semester") or "", placeholder="Ex: 2026.1")
                            new_desc  = st.text_area("Descrição",  value=s.get("description") or "", height=60)
                            save = st.form_submit_button("Salvar", type="primary")
                        if save:
                            try:
                                api.subjects_update(
                                    s["id"],
                                    name=new_name or None,
                                    professor=new_prof or None,
                                    schedule=new_sched or None,
                                    semester=new_sem or None,
                                    description=new_desc or None,
                                )
                                st.success("Atualizada!")
                                load_subjects()
                                st.rerun()
                            except Exception as e:
                                st.error(str(e))

                    with st.popover("🗄️ Arquivar"):
                        st.info(f"Arquivar **{s['name']}**?\nEla não aparecerá na lista ativa mas não será excluída.")
                        if st.button("Confirmar", key=f"arch_{s['id']}", type="primary"):
                            try:
                                api.subjects_update(s["id"], archived=True)
                                st.success("Arquivada!")
                                load_subjects()
                                st.rerun()
                            except Exception as e:
                                st.error(str(e))

                    with st.popover("🗑️ Excluir"):
                        st.warning(f"Excluir permanentemente **{s['name']}**?")
                        if st.button("Confirmar exclusão", key=f"del_{s['id']}", type="primary"):
                            try:
                                api.subjects_delete(s["id"])
                                st.success("Excluída!")
                                load_subjects()
                                st.rerun()
                            except Exception as e:
                                st.error(str(e))

# ════════════════════════════════════════════════════════════════════════════
# TAB: NOVA DISCIPLINA
# ════════════════════════════════════════════════════════════════════════════
with tab_novo:
    st.subheader("Cadastrar Nova Disciplina")

    if "subject_form_key" not in st.session_state:
        st.session_state["subject_form_key"] = 0

    with st.form(f"form_create_subject_{st.session_state['subject_form_key']}"):
        nome      = st.text_input("Nome da Disciplina *", placeholder="Ex: Cálculo I")
        professor = st.text_input("Nome do Professor",    placeholder="Ex: Dr. Silva")
        schedule  = st.text_input("Dia / Horário",        placeholder="Ex: Seg e Qua 08:00")
        semester  = st.text_input("Semestre / Período",   placeholder="Ex: 2026.1")
        description = st.text_area("Descrição (opcional)", height=80)
        submitted = st.form_submit_button("🌱 Cadastrar", type="primary", use_container_width=True)

    if submitted:
        if not nome.strip():
            st.warning("O nome da disciplina é obrigatório.")
        elif nome.strip().lower() in [s["name"].strip().lower() for s in active]:
            st.error(f"Já existe uma disciplina ativa chamada **{nome}**.")
        else:
            try:
                api.subjects_create(
                    name=nome.strip(),
                    professor=professor.strip() or None,
                    schedule=schedule.strip() or None,
                    semester=semester.strip() or None,
                    description=description.strip() or None,
                )
                st.success(f"✨ Disciplina **{nome}** criada com sucesso!")
                load_subjects()
                st.session_state["subject_form_key"] += 1
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao criar disciplina: {e}")

# ════════════════════════════════════════════════════════════════════════════
# TAB: BUSCAR
# ════════════════════════════════════════════════════════════════════════════
with tab_busca:
    st.subheader("Buscar Disciplinas")
    col_q, col_flag = st.columns([3, 1])
    with col_q:
        query_input = st.text_input("Buscar por nome, professor ou descrição", placeholder="ex: python…")
    with col_flag:
        st.markdown("<br>", unsafe_allow_html=True)
        include_overdue = st.checkbox("Apenas com tarefas atrasadas", value=False)

    if st.button("🔎 Buscar", type="primary", use_container_width=True):
        from datetime import datetime, timezone as tz
        now = datetime.now(tz=tz.utc)
        overdue_ids: set = set()
        for t in tasks:
            if t.get("status") == "completed":
                continue
            raw = t.get("due_date")
            if raw is None:
                continue
            try:
                if datetime.fromtimestamp(int(raw) / 1000, tz=tz.utc) < now:
                    overdue_ids.add(t.get("subject_id"))
            except Exception:
                pass

        q = query_input.strip().lower()
        results = []
        for s in active:
            nm = q and (q in s.get("name","").lower() or q in (s.get("professor") or "").lower() or q in (s.get("description") or "").lower())
            ov = include_overdue and s.get("id") in overdue_ids
            if not q and not include_overdue:
                results = active; break
            if nm or ov:
                results.append(s)

        st.markdown(f"**{len(results)} resultado(s)**")
        for s in results:
            ov_badge = f'<span class="badge-overdue">⚠ atrasada</span>' if s.get("id") in overdue_ids else '<span class="badge-ok">✓ Em dia</span>'
            st.markdown(
                f'<div class="fungi-card"><h4>{s["name"]} {ov_badge}</h4>'
                f'<p>{"👤 " + s.get("professor","") if s.get("professor") else ""}'
                f'{"  ·  📅 " + s.get("semester","") if s.get("semester") else ""}</p></div>',
                unsafe_allow_html=True,
            )
        if not results:
            st.info("Nenhuma disciplina encontrada.")

# ════════════════════════════════════════════════════════════════════════════
# TAB: ARQUIVADAS
# ════════════════════════════════════════════════════════════════════════════
with tab_archive:
    st.subheader("Disciplinas Arquivadas")
    if not archived:
        st.info("Nenhuma disciplina arquivada.")
    else:
        for s in archived:
            with st.expander(f'🗄️ {s["name"]} <span class="badge-archived">Arquivada</span>', expanded=False):
                col_i, col_a = st.columns([3, 1])
                with col_i:
                    st.markdown(f"**Professor:** {s.get('professor') or '—'}")
                    st.markdown(f"**Semestre:** {s.get('semester') or '—'}")
                with col_a:
                    if st.button("♻️ Desarquivar", key=f"unarch_{s['id']}"):
                        try:
                            api.subjects_update(s["id"], archived=False)
                            st.success("Desarquivada!")
                            load_subjects()
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
                    with st.popover("🗑️ Excluir"):
                        st.warning(f"Excluir permanentemente **{s['name']}**?")
                        if st.button("Confirmar", key=f"del_arch_{s['id']}", type="primary"):
                            try:
                                api.subjects_delete(s["id"])
                                load_subjects()
                                st.rerun()
                            except Exception as e:
                                st.error(str(e))
