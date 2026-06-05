import streamlit as st

import utils.xano_client as api

st.set_page_config(page_title="Disciplinas", page_icon="📚", layout="wide")

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

st.title("📚 Gestão de Disciplinas")

# ── Helper: load subjects into session cache ───────────────────────────────────
def load_subjects():
    try:
        st.session_state["subjects_cache"] = api.subjects_list()
    except Exception as e:
        st.error(f"Erro ao carregar disciplinas: {e}")
        st.session_state["subjects_cache"] = []

if "subjects_cache" not in st.session_state:
    load_subjects()

subjects: list = st.session_state.get("subjects_cache", [])

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_lista, tab_novo, tab_busca = st.tabs(["📋 Listar", "➕ Nova Disciplina", "🔍 Buscar"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB: LISTAR
# ════════════════════════════════════════════════════════════════════════════════
with tab_lista:
    col_refresh, _ = st.columns([1, 5])
    with col_refresh:
        if st.button("🔄 Atualizar", use_container_width=True):
            load_subjects()
            st.rerun()

    subjects = st.session_state.get("subjects_cache", [])

    if not subjects:
        st.info("Nenhuma disciplina cadastrada. Use a aba **Nova Disciplina** para começar.")
    else:
        for s in subjects:
            with st.expander(f"📚 {s['name']}", expanded=False):
                col_info, col_actions = st.columns([3, 1])

                with col_info:
                    st.markdown(f"**Professor:** {s.get('professor') or '—'}")
                    st.markdown(f"**Horário:** {s.get('schedule') or '—'}")
                    if s.get("description"):
                        st.markdown(f"**Descrição:** {s['description']}")

                with col_actions:
                    # Edit form
                    with st.popover("✏️ Editar"):
                        with st.form(f"edit_{s['id']}"):
                            new_name = st.text_input("Nome", value=s.get("name", ""))
                            new_prof = st.text_input("Professor", value=s.get("professor") or "")
                            new_sched = st.text_input("Horário", value=s.get("schedule") or "")
                            new_desc = st.text_input("Descrição", value=s.get("description") or "")
                            save = st.form_submit_button("Salvar", type="primary")
                        if save:
                            try:
                                api.subjects_update(
                                    s["id"],
                                    name=new_name or None,
                                    professor=new_prof or None,
                                    schedule=new_sched or None,
                                    description=new_desc or None,
                                )
                                st.success("Atualizada!")
                                load_subjects()
                                st.rerun()
                            except Exception as e:
                                st.error(str(e))

                    # Delete with confirmation
                    with st.popover("🗑️ Excluir"):
                        st.warning(f"Excluir **{s['name']}**?")
                        if st.button("Confirmar exclusão", key=f"del_{s['id']}", type="primary"):
                            try:
                                api.subjects_delete(s["id"])
                                st.success("Excluída!")
                                load_subjects()
                                st.rerun()
                            except Exception as e:
                                st.error(str(e))

# ════════════════════════════════════════════════════════════════════════════════
# TAB: NOVA DISCIPLINA
# ════════════════════════════════════════════════════════════════════════════════
with tab_novo:
    st.subheader("Cadastrar Nova Disciplina")

    with st.form("form_create_subject"):
        nome = st.text_input("Nome da Disciplina *", placeholder="Ex: Cálculo I")
        professor = st.text_input("Nome do Professor", placeholder="Ex: Dr. Silva")
        schedule = st.text_input("Dia / Horário", placeholder="Ex: Seg e Qua 08:00")
        description = st.text_area("Descrição (opcional)", height=80)
        submitted = st.form_submit_button("Salvar", type="primary", use_container_width=True)

    if submitted:
        if not nome.strip():
            st.warning("O nome da disciplina é obrigatório.")
        else:
            # Duplicate check
            existing_names = [s["name"].strip().lower() for s in subjects]
            if nome.strip().lower() in existing_names:
                st.error(f"Já existe uma disciplina chamada **{nome}**.")
            else:
                try:
                    api.subjects_create(
                        name=nome.strip(),
                        professor=professor.strip() or None,
                        schedule=schedule.strip() or None,
                        description=description.strip() or None,
                    )
                    st.success(f"Disciplina **{nome}** cadastrada com sucesso!")
                    load_subjects()
                except Exception as e:
                    st.error(f"Erro ao criar disciplina: {e}")

# ════════════════════════════════════════════════════════════════════════════════
# TAB: BUSCAR
# ════════════════════════════════════════════════════════════════════════════════
with tab_busca:
    st.subheader("Buscar Disciplinas")

    col_q, col_flag = st.columns([3, 1])
    with col_q:
        query_input = st.text_input(
            "Buscar por nome ou descrição",
            placeholder="ex: python, banco de dados…",
        )
    with col_flag:
        st.markdown("<br>", unsafe_allow_html=True)
        include_overdue = st.checkbox("Apenas com tarefas atrasadas", value=False)

    if st.button("🔎 Buscar", type="primary", use_container_width=True):
        with st.spinner("Buscando…"):
            try:
                results = api.subjects_search(
                    query=query_input,
                    include_overdue=include_overdue,
                )
                st.markdown(f"**{len(results)} resultado(s)**")
                if results:
                    for s in results:
                        st.markdown(
                            f'<div style="background:#1e293b;border:1px solid #334155;'
                            f'border-radius:10px;padding:.75rem 1rem;margin-bottom:.5rem">'
                            f'<b style="color:#e2e8f0">{s["name"]}</b>'
                            f'<br><span style="color:#94a3b8;font-size:.85rem">'
                            f'{s.get("professor","") or ""}'
                            f'{"  ·  " + s.get("schedule","") if s.get("schedule") else ""}'
                            f'</span></div>',
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("Nenhuma disciplina encontrada.")
            except Exception as e:
                st.error(f"Erro na busca: {e}")
