import streamlit as st

import utils.xano_client as api

st.set_page_config(page_title="Perfil", page_icon="👤", layout="centered")

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

st.title("👤 Meu Perfil")

# ── Load profile data ──────────────────────────────────────────────────────────
if "profile_data" not in st.session_state:
    try:
        st.session_state["profile_data"] = api.auth_me()
    except Exception as e:
        st.error(f"Erro ao carregar perfil: {e}")
        st.stop()

profile = st.session_state.get("profile_data", {})

# ── Display current info ───────────────────────────────────────────────────────
st.markdown("### Suas informações")
col1, col2 = st.columns(2)
col1.markdown(f"**Nome:** {profile.get('name', '—')}")
col2.markdown(f"**E-mail:** {profile.get('email', '—')}")
col1.markdown(f"**Função:** {profile.get('role', '—')}")

st.markdown("---")

# ── Edit form ──────────────────────────────────────────────────────────────────
st.markdown("### Editar informações")

with st.form("form_edit_profile"):
    new_name = st.text_input("Nome", value=profile.get("name", ""))
    new_email = st.text_input("E-mail", value=profile.get("email", ""))
    submitted = st.form_submit_button("Salvar alterações", type="primary", use_container_width=True)

if submitted:
    updates: dict = {}
    if new_name.strip() and new_name.strip() != profile.get("name"):
        updates["name"] = new_name.strip()
    if new_email.strip() and new_email.strip() != profile.get("email"):
        updates["email"] = new_email.strip()

    if not updates:
        st.info("Nenhuma alteração detectada.")
    else:
        try:
            result = api.user_edit_profile(
                name=updates.get("name"),
                email=updates.get("email"),
            )
            st.success("Perfil atualizado com sucesso!")
            st.session_state["profile_data"] = result
            st.session_state["user_name"] = result.get("name", new_name)
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao atualizar perfil: {e}")

st.markdown("---")

# ── Danger zone ────────────────────────────────────────────────────────────────
st.markdown("### Sessão")
if st.button("🚪 Encerrar sessão", type="secondary", use_container_width=True):
    st.session_state.clear()
    st.switch_page("app.py")
