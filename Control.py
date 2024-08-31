import sqlite3 as sql
import time
import pandas as pd
from fitness_tools.composition.bodyfat import JacksonPollock7Site

#cur.execute(''' 
#CREATE TABLE clientes (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE,
    #nome varchar(255) UNIQUE NOT NULL, idade int NOT NULL, telefone varchar(25) NOT NULL,
    #sexo varchar(255) CHECK(sexo IN("Masculino", "Feminino", "Outro")))
 #''')

#cur.execute('''
    #CREATE TABLE dados (data DATE NOT NULL, nome_clientes varchar(255) NOT NULL, 
        #peso int NOT NULL, altura INT NOT NULL, ombro int NOT NULL, braco_d_relx INT NOT NULL, 
        #braco_e_relx INT NOT NULL,braco_d_cont INT NOT NULL, braco_e_cont INT NOT NULL, 
        #ante_braco_d INT NOT NULL, ante_braco_e INT NOT NULL,torax_relx INT NOT NULL, torax_insp INT NOT NULL, 
        #cintura INT NOT NULL, abdomen INT NOT NULL,quadril INT NOT NULL, coxa_d INT NOT NULL, coxa_e INT NOT NULL, 
        #panturrilha_d INT NOT NULL,panturrilha_e INT NOT NULL, subescapular INT NOT NULL, tricipital INT NOT NULL, 
        #axilar_media INT NOT NULL,supra_iliaca INT NOT NULL, peitoral INT NOT NULL, abdominal INT NOT NULL,
        #coxa_dobcut INT NOT NULL, FOREIGN KEY (nome_clientes) REFERENCES clientes(nome)) ''')


def conectar():
    con = sql.connect("banco.db")
    return con

#### CLIENTES
def cadastrar_clientes(nome, idade, telefone, sexo):
    con = conectar()
    cur = con.cursor()

    cur.execute(f'INSERT INTO clientes (nome, idade, telefone, sexo) VALUES ("{nome}","{idade}","{telefone}","{sexo}")')

    con.commit()
    cur.close()
    con.close()

    return "Cadastrado com sucesso!"

def atualizar_clientes(nome, idade, telefone, sexo):
    con = conectar()
    cur = con.cursor()

    cur.execute(f'UPDATE clientes SET nome = "{nome}", idade = "{idade}", telefone = "{telefone}", sexo = "{sexo}"')

    con.commit()
    cur.close()
    con.close()
    return "Dados atualizados"

def deletar_clientes(nome):
    con = conectar()
    cur = con.cursor()

    try:
        cur.execute(f"DELETE FROM clientes WHERE nome = '{nome}'")
        cur.execute(f"DELETE FROM dados WHERE nome_clientes = '{nome}'")
    except sql.OperationalError:
        print("Excluiu mas não tem dados")
        cur.execute(f"DELETE FROM clientes WHERE nome = '{nome}'")

    con.commit()
    cur.close()
    con.close()

    return "Cliente deletado com sucesso"

def visu_clientes():
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT * FROM clientes")
    result = cur.fetchall()
    
    cabecalho = ['ID', 'NOME', 'IDADE', 'TELEFONE','SEXO']
    df = pd.DataFrame(result, columns = cabecalho)
    con.commit()
    cur.close()
    con.close()

    return df
    
#### DADOS

def cadastrar_dados(data, nome_clientes, peso, altura,ombro, braco_d_relx, braco_e_relx, braco_d_cont,braco_e_cont,ante_braco_d, ante_braco_e,torax_relx,torax_insp, cintura, abdomen, quadril,coxa_d,coxa_e,panturrilha_d,panturrilha_e,subescapular,tricipital,axilar_media,supra_iliaca,peitoral,abdominal,coxa_dobcut):
    con = conectar()
    cur = con.cursor()

    cur.execute(f'''INSERT INTO dados (data, nome_clientes, peso, altura,ombro, braco_d_relx, braco_e_relx, braco_d_cont,braco_e_cont,ante_braco_d, ante_braco_e,torax_relx,torax_insp, cintura, abdomen, quadril,coxa_d,coxa_e,panturrilha_d,panturrilha_e,subescapular,tricipital,axilar_media,supra_iliaca,peitoral,abdominal,coxa_dobcut)
        VALUES ("{data}","{nome_clientes}","{peso}","{altura}","{ombro}","{braco_d_relx}","{braco_e_relx}","{braco_d_cont}","{braco_e_cont}","{ante_braco_d}","{ante_braco_e}","{torax_relx}","{torax_insp}","{cintura}","{abdomen}","{quadril}","{coxa_d}","{coxa_e}","{panturrilha_d}","{panturrilha_e}","{subescapular}","{tricipital}","{axilar_media}","{supra_iliaca}","{peitoral}","{abdominal}","{coxa_dobcut}")''')
    
    con.commit()
    cur.close()
    con.close()

    return'dados cadastrados'

def visu_dados():
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT * FROM dados")

    result = cur.fetchall()

    cabecalho = ['data', 'nome_clientes', 'peso', 'altura', 'ombro', 'braco_d_relx', 'braco_e_relx', 'braco_d_cont', 'braco_e_cont', 'ante_braco_d', 'ante_braco_e', 'torax_relx', 'torax_insp', 'cintura', 'abdomen', 'quadril', 'coxa_d', 'coxa_e', 'panturrilha_d', 'panturrilha_e', 'subescapular', 'tricipital', 'axilar_media','supra_iliaca', 'peitoral', 'abdominal', 'coxa_dobcut']
    df = pd.DataFrame(result, columns= cabecalho)
    cur.close()
    con.close()

    return df

def deletar_dados(data, nome):
    con = conectar()
    cur = con.cursor()
    
    cur.execute(f'DELETE FROM dados WHERE data = "{data}" AND nome_clientes ="{nome}"')

    con.commit()
    cur.close()
    con.close()
    return "Dados deletados"

def imc():

    data = {
        "IMC": ["Abaixo de 18", "18,5 a 24,9","25 a 29,9","30 a 34,9","35 a 39,9","Maior que 40"],
        "Classificação": ["Abaixo do Normal","Normal", "Sobrepeso", "Obesidade grau I","Obesidade grau II","Obesidade grau III"]
    }

    df = pd.DataFrame(data)
    df = df.to_html(index=False)

    return df

def rcq():

    data = {
        "Classificação": ["Baixo","Normal", "Alto"],
        "Feminino":["Abaixo de 0,80", "0,81 a 0,85", "Maior que 0,86"],
        "Masculino":["Abaixo de 0,95", "0,96 a 1,00", "Maior que 1,00"]
    }
    
    df = pd.DataFrame(data)
    df = df.to_html(index=False)

    return df

def pct_gordura():
    
    data = {
        
        "Descrição":["Gordura Essencial","Atletas", "Praticantes de Atividades", "Aceitavel", "Obesidade"],
        "Mulher":['10 a 13%', "14 a 20%", "21 a 24%","25 a 31%", "Acima de 32%"],
        "Homem":['2 a 5%', "6 a 13%", "14 a 17%", "18 a 24%", "Acima de 25%"]
    }
    
    df = pd.DataFrame(data)
    df = df.to_html(index=False)
    return df


def calc_massagorda(row):
    row['Percentual Gordura'] = row['Percentual Gordura']/100
    
    massagorda = row['peso'] * row['Percentual Gordura']
    return massagorda
    
def calc_massamagra(row):

    massamagra = row['peso'] - row['massagorda']
    
    return massamagra

def calc_massagorda_magra(row):

    row['Percentual Gordura'] = row['Percentual Gordura']/100
    massagorda = row['peso'] * row['Percentual Gordura']

    massamagra = row['peso'] - massagorda


    return massagorda, massamagra

def calc_percentual_gordura_7(row):

    dobras = [
        row['subescapular'],
        row['tricipital'],
        row['axilar_media'],
        row['supra_iliaca'],
        row['peitoral'],
        row['abdominal'],
        row['coxa_dobcut']
    ]
    if row['SEXO'] == 'Masculino':
        
        dc = JacksonPollock7Site(row['IDADE'], 'male', (dobras))
    if row['SEXO'] == 'Feminino':
        
        dc = JacksonPollock7Site(row['IDADE'], 'female', (dobras))

    dc_val = dc.body_density()
    bf = (495 / dc_val) - 450

    return bf
