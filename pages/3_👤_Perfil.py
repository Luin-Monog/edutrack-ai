import streamlit as st

import utils.xano_client as api
from utils.theme import SPORE_DIVIDER

st.markdown("# 👤 Meu Perfil")
st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)

if "profile_data" not in st.session_state:
    try:
        st.session_state["profile_data"] = api.auth_me()
    except Exception as e:
        st.error(f"Erro ao carregar perfil: {e}")
        st.stop()

profile = st.session_state.get("profile_data", {})

st.markdown("### ✦ Suas informações")
col1, col2 = st.columns(2)
col1.markdown(f"**Nome:** {profile.get('name', '—')}")
col2.markdown(f"**E-mail:** {profile.get('email', '—')}")
col1.markdown(f"**Função:** {profile.get('role', '—')}")

st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)
st.markdown("### ✏️ Editar informações")

with st.form("form_edit_profile"):
    new_name  = st.text_input("Nome",   value=profile.get("name", ""))
    new_email = st.text_input("E-mail", value=profile.get("email", ""))
    submitted = st.form_submit_button("Salvar alterações", type="primary", use_container_width=True)

if submitted:
    updates: dict = {}
    if new_name.strip()  and new_name.strip()  != profile.get("name"):  updates["name"]  = new_name.strip()
    if new_email.strip() and new_email.strip() != profile.get("email"): updates["email"] = new_email.strip()
    if not updates:
        st.info("Nenhuma alteração detectada.")
    else:
        try:
            result = api.user_edit_profile(name=updates.get("name"), email=updates.get("email"))
            st.success("Perfil atualizado!")
            st.session_state["profile_data"] = result
            st.session_state["user_name"] = result.get("name", new_name)
            st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")

st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)
st.markdown("### 🔐 Alterar senha")

with st.form("form_change_password"):
    new_pass     = st.text_input("Nova senha (mín. 8 caracteres)", type="password")
    confirm_pass = st.text_input("Confirmar nova senha",           type="password")
    pass_submitted = st.form_submit_button("Alterar senha", type="primary", use_container_width=True)

if pass_submitted:
    if not new_pass or not confirm_pass:
        st.warning("Preencha os dois campos.")
    elif len(new_pass) < 8:
        st.warning("Mínimo 8 caracteres.")
    elif new_pass != confirm_pass:
        st.error("As senhas não coincidem.")
    else:
        try:
            api.auth_update_password(new_pass, confirm_pass, st.session_state["token"])
            st.success("✨ Senha alterada com sucesso!")
        except Exception as e:
            st.error(f"Erro: {e}")

st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)
st.markdown("### 🚪 Sessão")
if st.button("Encerrar sessão", type="secondary", use_container_width=True):
    st.session_state.clear()
    st.switch_page("app.py")
