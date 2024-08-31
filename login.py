import streamlit as st
from time import sleep
from navigation import make_sidebar

st.set_page_config(layout="wide")

st.title("Bem vindo")
st.write("Sistema de Avaliação Fisica)
username = st.text_input("Usuario:")
password = st.text_input("Senha:", type="password")

if st.button("Log in", type="primary"):

    if username == "luan" and password == "112233":
        st.session_state.logged_in = True
        st.success("Login realizado com sucesso!")
        sleep(0.5)
        st.switch_page("pages/Home.py")
    else:
        st.error("Usuario ou senha incorretos")

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("Desenvolvido e mantido por @Bruno Andrade Lourenço")
