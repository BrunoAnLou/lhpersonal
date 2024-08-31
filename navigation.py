import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/Home.py", label="Home")
            st.page_link("pages/Gestão_de_Dados.py", label="Gestão de Dados")
            st.page_link("pages/Visão_Geral.py", label="Visão Geral")
            st.write("")
            st.write("")

            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            if st.button("Logoff"):
                logout()

            st.write("")
            st.write("@Bruno Andradade Lourenço")
        elif get_current_page_name() != "login":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("login.py")


def logout():
    st.session_state.logged_in = False
    st.info("Deslogado com sucesso!")
    sleep(0.5)
    st.switch_page("login.py")