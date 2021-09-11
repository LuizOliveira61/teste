import time

import streamlit as st
import datetime
from PIL import Image
import sqlite3

#==============================
def conectar_db():

    con = sqlite3.connect('jetclub.db')
    cursor = con.cursor()

    return con, cursor


def cria_db():
    con = sqlite3.connect('jetclub.db')
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS jetclub
                      (cota UNIQUE, login UNIQUE, senha, nome, lanchas, status, agenda)''')
    con.commit()
    con.close()


def add_login(cota, login, senha, nome, lanchas, status, agenda):
    con, cursor = conectar_db()
    cursor.execute(f'INSERT INTO jetclub VALUES ({cota}, "{login}", "{senha}", "{nome}", "{lanchas}", "{status}", "{agenda}")')

    con.commit()
    con.close()


def consultar_db(login):
    con, cursor = conectar_db()

    pesquisa = cursor.execute(f"select * from jetclub WHERE login = '{login}'")
    infos = pesquisa.fetchall()
    #print(infos)
    senha = infos[0][2]
    nome = infos[0][3]
    lanchas = infos[0][4]
    status = infos[0][5]
    agenda = infos[0][6]

    #print(agenda)

    con.commit()
    con.close()

    return nome, senha, lanchas, status, agenda

#add_login(3, 'vicmendon', '123', 'Victor', ['Itaipu','Paquetá'], 'Pago', ' ')

def conserta_data(info, nova_data):
    lista = []
    info = info.replace("'",'').replace('\\','').replace('\t','').replace(' ','').replace('[','').replace(']','')
    info = info.split(',')
    lista.append(nova_data)
    for x in info:
        lista.append(x)
    lista = str(lista)
    lista = lista.replace("'",'').replace('\\','').replace('\t','').replace(' ','').replace('[','').replace(']','')
    return lista


def add_data(login, data):
    con, cursor = conectar_db()

    nome, senha, lanchas, status, agenda = consultar_db(login)

    agenda_nova = conserta_data(agenda, data)

#    agenda.append(data)

#    agenda = str(agenda)

    cursor.execute(f"UPDATE jetclub SET agenda = '{agenda_nova}' WHERE login = '{login}'")
    #cursor.execute(f"INSERT INTO jetclub VALUES ('{data}')")

    con.commit()
    con.close()


def conserta_data2(info, nova_data):
    lista = []
    info = info.replace("'",'').replace('\\','').replace('\t','').replace(' ','').replace('[','').replace(']','')
    info = info.split(',')
    for x in info:
        if nova_data != x:
            lista.append(x)
    lista = str(lista)
    lista = lista.replace("'",'').replace('\\','').replace('\t','').replace(' ','').replace('[','').replace(']','')
    return lista


def remove_data(login, data):
    con, cursor = conectar_db()

    nome, senha, lanchas, status, agenda = consultar_db(login)

    agenda_nova = conserta_data2(agenda, data)

#    agenda.append(data)

#    agenda = str(agenda)

    cursor.execute(f"UPDATE jetclub SET agenda = '{agenda_nova}' WHERE login = '{login}'")
    #cursor.execute(f"INSERT INTO jetclub VALUES ('{data}')")

    con.commit()
    con.close()

def consultar_marcados(lancha):
    con, cursor = conectar_db()

    datas_marcadas = []

    pesquisa = cursor.execute(f"select * from jetclub WHERE lanchas = '{lancha}'")
    infos = pesquisa.fetchall()
    senha = infos[0][2]
    nome = infos[0][3]
    lanchas = infos[0][4]
    status = infos[0][5]
    agenda = infos[0][6]

    for x in infos:
        #print(x[6])
        datas = x[6].split(',')
        for y in datas:
            datas_marcadas.append(y)

    print(datas_marcadas)

    con.commit()
    con.close()

    return datas_marcadas
#==============================

image = Image.open('foto.jpg')


st.title('Agendamento JetClub')

st.image(image, use_column_width=True)

login = st.sidebar.text_input(label='Login')

senha_digitada = st.sidebar.text_input(label='Senha', type='password')

try:
    nome, senha, lanchas, status, agenda = consultar_db(login)
except Exception as e:
    pass

cotista = 'Não encontrado'

try:
    if senha == senha_digitada:
        cotista = nome
        status = status
        agendados = agenda
except Exception as e:
    if senha_digitada == '':
        pass
    elif senha_digitada != senha:
        st.sidebar.error('Senha incorreta!')

if cotista != 'Não encontrado':
    st.sidebar.text(f'Bem vindo, {cotista}')

    st.sidebar.text('Agendamentos')

    marcados = consultar_marcados(lanchas)

    agendados = agendados.split(',')


    for x in agendados:
        if x != '':
            #col1, col2 = st.sidebar.columns([2,1])
            #col1.text(x)
            form = st.sidebar.form(key = x)
            form.text(f'Data agendada: {x}')
            submit = form.form_submit_button('Remover Agendamento')
            #col2.submit
            if submit:
                remove_data(login, x)
                form.success('Data removida com sucesso!')
                time.sleep(.3)
                st.experimental_rerun()

    data = st.date_input(label='Data')

    dia = data.day
    mes = data.month
    ano = data.year

    marcacao = f'{dia}/{mes}/{ano}'

    agendamento = ''

    agendado = False

    for x in marcados:
        if marcacao == x:
            st.error(f'Dia {marcacao} já agendado!')
            agendado = True

    if agendado == False:
        if st.button('Reservar') and agendado == False:
            if status == 'Pago':

                marcou = 0
                for x in agendados:
                    agendar = f'{data.month}/{data.year}'
                    if agendar in x:
                        marcou +=1
                if marcou >= 3:
                    st.error('Limite mensal esgotado!')
                else:
                    add_data(login, marcacao)
                    st.success(f'Reserva realizada com sucesso para o dia {marcacao}!')
                    time.sleep(3)
                    st.experimental_rerun()

            if status == 'Devedor':
                st.error('Acerte a sua mensalidade!')
    st.success(marcados)
