import sqlite3 as sql
import streamlit as st
import pandas as pd
import time
from st_aggrid import AgGrid, GridOptionsBuilder
from Control import conectar, cadastrar_clientes, atualizar_clientes, deletar_clientes, visu_clientes, cadastrar_dados, visu_dados, deletar_dados
from navigation import make_sidebar


make_sidebar()


st.title("Gestão de Dados")
st.write("Cadastrar, excluir e consultar informações de alunos, e dos dados de aferição.")
###############################################################################################################

tab1, tab2, tab3, tab4 = st.tabs(["Cadastrar","Dados","Excluir", "Consultar"])

with tab1:
    st.subheader("Cadastro de Aluno")
    nome = st.text_input("Insira nome:")
    idade = st.text_input("Insira idade:")
    tel = st.text_input("Insira telefone:")
    sexo = st.selectbox("Selecione sexo:", ['Masculino', 'Feminino', 'Outro'])

    if st.button("Cadastrar"):
        try:

            if nome and idade and tel and sexo:
                cad = cadastrar_clientes(nome, idade, tel, sexo)
                st.success("Cliente cadastrado com sucesso")
            else:
                st.error("Verifique as informações prestadas, e tente novamente")
        except sql.IntegrityError:
            st.error("Usuario já cadastrado!")
with tab2:
    st.subheader("Cadastro de Dados")
    db_clientes = visu_clientes()
    db_dados = visu_dados()

    df = pd.DataFrame(db_clientes)
    df2 = pd.DataFrame(db_dados)

    col1, col2, col3 = st.columns(3)

    data = col1.date_input("Data da aferição:", format="DD/MM/YYYY")
    nome = col2.selectbox("Selecione o aluno:", df['NOME'])
    peso = col1.number_input("Peso:")
    altura = col2.number_input("Altura (ex: 1,90):")
    st.write("")

    st.subheader("Circunferência")

    col1 , col2, col3, col4 =st.columns(4)

    ombro = col1.text_input("Ombro:")
    braco_d_relx = col2.text_input("Braço direito relaxado:")
    braco_e_relx = col3.text_input("Braço esquerdo relaxado:")
    braco_d_cont = col4.text_input("Braço direito contraido:")
    braco_e_cont = col1.text_input("Braço esquerdo contraido:")
    ante_braco_d = col2.text_input("Antebraço direito:")
    ante_braco_e = col3.text_input("Antebraço esquerda:")
    torax_relx = col4.text_input("Torax relaxado:")
    torax_insp = col1.text_input("Torax inspirado:")
    cintura = col2.text_input("Cintura:")
    abdomen = col3.text_input("Abdomen:")
    quadril = col4.text_input("Quadril:")
    coxa_d = col1.text_input("Coxa direita:")
    coxa_e = col2.text_input("Coxa esquerda:")
    panturrilha_d = col3.text_input("Panturrilha Direita:")
    panturrilha_e = col4.text_input("Panturrilha Esquerda:")
    st.write("")

    st.subheader("Dobras Cutaneas")
    col1, col2, col3, col4 = st.columns(4)
    subescapular = col1.text_input("Subescapular:")
    tricipital = col2.text_input("Tripicital:")
    axilar_media = col3.text_input("Axilar-Media:")
    supra_iliaca = col4.text_input("Supra ilíaca:")
    peitoral = col1.text_input("Peitoral:")
    abdominal = col2.text_input("Abdominal:")
    coxa_dobcut= col3.text_input("Coxa")

    if st.button("Inserir Dados"):
        try:
            if data and nome and peso and altura and ombro and braco_d_relx and braco_e_relx and braco_d_cont and braco_e_cont and ante_braco_d and ante_braco_e and torax_relx and torax_insp and cintura and abdomen and quadril and coxa_d and coxa_e and panturrilha_d and panturrilha_e and subescapular and tricipital and axilar_media and supra_iliaca and peitoral and abdominal and coxa_dobcut:
    
                cad = cadastrar_dados(data, nome, peso, altura,ombro, braco_d_relx, braco_e_relx, braco_d_cont,braco_e_cont,ante_braco_d,ante_braco_e,torax_relx,torax_insp, cintura, abdomen, quadril,coxa_d,coxa_e,panturrilha_d,panturrilha_e,subescapular,tricipital ,axilar_media,supra_iliaca,peitoral,abdominal,coxa_dobcut)
                st.success("Dados cadastrados com sucesso!")
                
            else:
                st.error("Verifique as informações e tente novamente")
        except sql.IntegrityError:
            st.error("Verifique os dados e tente novamente")



with tab3:
    select = st.radio("Escolha uma opção", ['Cadastro', 'Dados'])

    clientes = df['NOME'].unique()
    

    if select == 'Cadastro':
        select_cli = st.selectbox("Selecione o aluno a ser excluido:", clientes)

        if st.button("Deletar"):
            if select_cli:
                deletar_clientes(select_cli)
                st.success("Aluno deletado com sucesso!")
                
    if select == 'Dados':
        col1 , col2 = st.columns(2)
        
        clientes = df2['nome_clientes'].unique()
        select_dado = col1.selectbox("Selecione o aluno a qual você deseja deletar os dados:", clientes)
        
        datas_clientes = df2.loc[df2['nome_clientes'] == select_dado, 'data']
        data = col2.selectbox("Selecione a data da aferição que deseja apagar:", datas_clientes.values)


        if st.button("Deletar"):
            if data and select_dado:
                deletar_dados(data, select_dado)
                st.rerun()
                time.sleep(1)
                st.success("Deu boa")

with tab4:
    
    clientes_db = visu_clientes()
    dados_db = visu_dados()
    df = pd.DataFrame(clientes_db)
    df_dados = pd.DataFrame(dados_db)

    clientes = st.selectbox("Selecione clientes",['Clientes', 'Dados'])

    if clientes == 'Clientes':
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize = True)
        gb.configure_column("ID", width=100)
        gb.configure_column("NOME", width=450)
        gb.configure_column("IDADE", width=120)
        gridOptions = gb.build()

        AgGrid(df, gridOptions = gridOptions, fit_columns_on_grid_load=True)

    if clientes == 'Dados':
        gb = GridOptionsBuilder.from_dataframe(df_dados)
        gb.configure_pagination(paginationAutoPageSize = True)
        gridOptions = gb.build()
        AgGrid(df_dados, gridOptions = gridOptions)


