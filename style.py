import streamlit as st
import base64
from docx import Document

def alinhar():
    st.markdown("""
        <style>
        th {
            text-align: left;
        }
        </style>
        """, unsafe_allow_html=True)


def imc_calc(imc):
    if imc < 18.5:
        return "<span style='color: #5924d6;'>Abaixo do Normal</span>"
    
    elif 18.5 <= imc <24.9:
        return "<span style='color: #36d624;'>Normal</span>"

    elif 25 <= imc <29.9:
        return "<span style='color: #f0de1f;'>Sobrepeso</span>"

    elif 30 <= imc <34.9:
        return "<span style='color: #e0773f;'>Obesidade Grau I</span>"

    elif 35 <= imc <39.9:
        return "<span style='color: red;'>Obesidade Grau II</span>"

    else:
        return "<span style='color: #81319e;'>Obesidade Grau III</span>"


def calc_rcq(rcq, sexo):

    if sexo == 'Feminino':
        if rcq <= 0.80:
            return "<span style='color: #5924d6;'>Baixo</span>"
            
        if rcq > 0.81 and rcq <=0.85:
            return "<span style='color: #5924d6;'>Normal</span>"
            
        if rcq >=0.86:
            return "<span style='color: #5924d6;'>Alto</span>"
            

    if sexo == 'Masculino':

        if rcq >= 0.96 and rcq <= 0.99:
            return "<span style='color: green ;'>Normal</span>"
            
        if rcq < 0.95:
            return "<span style='color: blue;'>Baixo</span>"

        else:
            return "<span style='color: red;'>Alto</span>"
           
