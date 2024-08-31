import streamlit as st
import pandas as pd
import plotly_express as px
from Control import visu_dados, visu_clientes, imc, rcq ,pct_gordura, calc_percentual_gordura_7, calc_massagorda, calc_massamagra
from style import alinhar, imc_calc, calc_rcq
from docx import Document
from navigation import make_sidebar

make_sidebar()


st.title("Visão Geral do Aluno")

###################################


clientes = visu_clientes()
df_alunos = pd.DataFrame(clientes)

dados = visu_dados()
df_dados = pd.DataFrame(dados)
df_dados.rename(columns={'nome_clientes':'NOME'}, inplace=True)


####################################
col1, col2 = st.columns(2)

####CALCULOS####

df_dados['IMC'] = df_dados['peso']/(df_dados['altura']*df_dados['altura'])
df_dados['RCQ'] =df_dados['quadril']/df_dados['cintura']
df_dados['Soma Dobras'] = df_dados['subescapular'] + df_dados['tricipital'] + df_dados['axilar_media'] + df_dados['supra_iliaca'] + df_dados['peitoral'] + df_dados['abdominal'] + df_dados['coxa_dobcut']
#dobras = df_dados[['subescapular','tricipital','axilar_media','supra_iliaca','peitoral','abdominal','coxa_dobcut']]


####

df_final = pd.merge(df_alunos, df_dados, on = 'NOME')

####CALCULOS
df_final['Percentual Gordura'] = df_final.apply(calc_percentual_gordura_7, axis=1)
df_final['massagorda'] = df_final.apply(calc_massagorda, axis=1)
df_final['massamagra'] = df_final.apply(calc_massamagra, axis=1)

df_final['IMC'] = df_final['peso']/(df_final['altura']*df_final['altura'])
df_final['RCQ'] =df_final['quadril']/df_final['cintura']


#Seleciona aluno do df_final com os nomes unificados
alunos_select = st.selectbox("Escolha um aluno:", df_final['NOME'].unique())

####
data_cliente = df_final[df_final['NOME']== alunos_select]['data'].unique()
filtro_dados = df_final[df_final['NOME'] == alunos_select]
ultima_data = filtro_dados[filtro_dados['data'] ==  filtro_dados['data'].max()]


dados_circ = filtro_dados.melt(id_vars=['data','NOME'], value_vars=['ombro', 'braco_d_relx', 'braco_e_relx', 'braco_d_cont', 'braco_e_cont', 'ante_braco_d', 'ante_braco_e', 'torax_relx', 'torax_insp', 'cintura', 'abdomen', 'quadril', 'coxa_d', 'coxa_e', 'panturrilha_d', 'panturrilha_e'], var_name="Metrica", value_name="Valor")
dados_dobras = filtro_dados.melt(id_vars=['data','NOME'], value_vars=[ 'subescapular', 'tricipital', 'axilar_media','supra_iliaca', 'peitoral', 'abdominal', 'coxa_dobcut'], var_name="Metrica", value_name="Valor")
outros_dados = filtro_dados.melt(id_vars=['data','NOME'], value_vars=['massagorda','massamagra'], var_name="Metrica", value_name="Valor")


dados_circ_ultimo = ultima_data.melt(id_vars=['data','NOME'], value_vars=['ombro', 'braco_d_relx', 'braco_e_relx', 'braco_d_cont', 'braco_e_cont', 'ante_braco_d', 'ante_braco_e', 'torax_relx', 'torax_insp', 'cintura', 'abdomen', 'quadril', 'coxa_d', 'coxa_e', 'panturrilha_d', 'panturrilha_e'], var_name="Metrica", value_name="Valor")
dados_dobras_ultimo  = ultima_data.melt(id_vars=['data','NOME'], value_vars=['subescapular', 'tricipital', 'axilar_media','supra_iliaca', 'peitoral', 'abdominal', 'coxa_dobcut'], var_name="Metrica", value_name="Valor")
outros_dados_ultimo  = ultima_data.melt(id_vars=['data','NOME'], value_vars=['peso'], var_name="Metrica", value_name="Valor")

tab1, tab2 = st.tabs(['Dados', 'Evolução'])

with tab1:


    ultima_Data = filtro_dados['data'].values[-1]
    st.write(f"Dados da ultima aferição: {ultima_Data}")

    st.write(f"Aluno: {filtro_dados['NOME'].values[-1]}")
    st.write(f"Peso Atual: {filtro_dados['peso'].values[-1]}")
    st.write(f"Altura: {filtro_dados['altura'].values[-1]} m")
    st.write(f"Idade: {filtro_dados['IDADE'].values[-1]} anos")

    st.header("Resumo dos dados:")
    st.write(f"Dados da ultima aferição no dia {ultima_Data}")

    col1, col2 = st.columns(2)
    
#filtro_dados = df_final[df_dados['NOME'] == alunos_select]

####IMC

    imc = imc()
    alinhar()

    imc_Dado=filtro_dados['IMC'].values[-1]

    classi_imc = imc_calc(imc_Dado)

    col1.subheader(F"IMC: {imc_Dado:.2f}")
    col1.write(f"Aluno(a), e está atualmente classificado como {classi_imc}, conforme tabela abaixo:", unsafe_allow_html=True)

    col1.markdown(imc, unsafe_allow_html=True)


###rcq
    rcq = rcq()
    rcq_texto = filtro_dados['RCQ'].values[-1]
    rcq_dado= filtro_dados['RCQ']
    rcq_sexo = filtro_dados['SEXO']
    rcq_dado_loc = rcq_dado.iloc[-1]
    rcq_sexo_loc = rcq_sexo.iloc[-1]

    class_rcq = calc_rcq(rcq_dado_loc,rcq_sexo_loc)

    col2.subheader(f"RCQ: {rcq_texto:.2f}")
    col2.write(f"Aluno(a), e está atualmente classificado como {class_rcq}, conforme tabela abaixo:", unsafe_allow_html=True)

    col2.markdown(rcq, unsafe_allow_html=True)

    ###Circunferencias 
    st.subheader("Circunferências")
    st.write("Gráfico das circunferências atuais do aluno")

    fig =px.bar(dados_circ_ultimo,x='Metrica', y ='Valor',text_auto='')
    fig.update_layout(xaxis_tickangle=-45, template="plotly_dark")
    fig

    ##Dobras Cutaneas

    fig2 = px.bar(dados_dobras_ultimo,x='Metrica', y ='Valor',text_auto='inside')
    fig2.update_layout(xaxis_tickangle=-45, template="plotly_dark")


    st.subheader("Dobras Cutaneas")
    st.write("Gráfico das dobras cutaneas atuais do aluno")
    fig2









    ## ##### DENSIDADE CORPORAL#########
    st.subheader("Densidade Corporal")

    pct_gordura = pct_gordura()

    st.write(F"Percentual de gordura atual do Aluno(a) {filtro_dados['Percentual Gordura'].values[-1]:.2f}% ", unsafe_allow_html=True)


    st.write(pct_gordura, unsafe_allow_html=True)


    st.write(" ")
    st.write("Massas:")
    st.write(f" * Massa gorda: {filtro_dados['massagorda'].values[-1]:.2f}kg ")
    st.write(f" * Massa gorda: {filtro_dados['massamagra'].values[-1]:.2f}kg ")

    col1, col2 = st.columns(2)

    fig_gord = px.pie(values=[filtro_dados['massagorda'].values[-1],filtro_dados['massamagra'].values[-1]], names=['Massa Gorda','Massa Magra'], title = "Massa Gorda x Massa Magra")
    col1.write(fig_gord)










with tab2:
    col1, col2, col3 = st.columns(3)

    fig1 = px.line(filtro_dados, x='data', y='peso', title = 'Peso', text= 'peso')
    fig1.update_traces(textposition='top center')
    fig1.update_xaxes(type='category')
    fig1.update_layout(yaxis=dict(range=[0,200]))

    col1.write(fig1)

    fig2 = px.bar(filtro_dados, x= 'data', y ='IMC', color = 'data', title= 'IMC', text_auto='')
    fig2.update_traces(textposition='auto')
    fig2.update_xaxes(type='category')
    col2.write(fig2)

    fig3 = px.bar(filtro_dados, x= 'data', y ='RCQ', color = 'data', title= 'RCQ', text_auto='')
    fig3.update_xaxes(type='category')    
    col3.write(fig3)


    ######## SUPERIOR ##########
    st.subheader("Circunferência ")

    fig4 =px.bar(dados_circ,x='Metrica', y ='Valor',color = 'data',text_auto='') #,  color_discrete_sequence= px.colors.qualitative.Plotly)
    fig4.update_layout(xaxis_tickangle=-45, template="plotly_dark")
    fig4

    st.subheader("Dobra Cutaneas ")

    fig5=px.bar(dados_dobras,x='Metrica', y ='Valor',color = 'data',text_auto='')#, color_discrete_sequence= px.colors.qualitative.Plotly)
    fig5.update_layout(xaxis_tickangle=-45, template="plotly_dark")
    fig5


    #######densidade    
    st.subheader("Densidade Corporal")
    col1, col2 = st.columns(2)


    
    fig6=px.bar(filtro_dados,x='data', y ='Percentual Gordura',color = 'data',text_auto='', title="Percentual de gordura")#, color_discrete_sequence= px.colors.qualitative.Plotly)
    fig6.update_layout(xaxis_tickangle=-45, template="plotly_dark")
    fig6.update_xaxes(type='category')
    col1.write(fig6)


    
    fig7=px.line(outros_dados,x='data',y='Valor', color = 'Metrica', title="Grafico de evolução: Massa Magra x Massa Gorda")#, color_discrete_sequence= px.colors.qualitative.Plotly)
    fig7.update_layout(template="plotly_dark")
    fig7.update_xaxes(type='category')
    col2.write(fig7)   



nome = str(filtro_dados['NOME'].values[-1])
idade = str(filtro_dados['IDADE'].values[-1])
IMC = str(filtro_dados['IMC'].values[-1].round(2))
RCQ = str(filtro_dados['RCQ'].values[-1])
nome
idade
IMC

referencias = {
    "$aluno$":nome,
    "$idade$":idade,
    "$IMC$":IMC,
    "$RCQ$":RCQ
}




