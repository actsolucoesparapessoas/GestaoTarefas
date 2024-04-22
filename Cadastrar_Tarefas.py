#TO SEND A E-MAIL WITH AN ATTACHMENT
#lINK: https://mailtrap.io/blog/python-send-email-gmail/
import streamlit as st
import pandas as pd
import sqlite3
import sqlite3 as sq
from PIL import Image
#import openpyxl
import urllib3
from urllib3 import request
from pathlib import Path
import time
import pytz
import datetime
from datetime import datetime
from Send2MaillMSK import Send2Mail, IsNiver

global MAIL, SENHA, MAIL2BOARD

# Page setting
st.set_page_config(layout="wide", page_title="Gestão de TAREFAS")

# storing the current time in the variable
c = datetime.now()
D = pd.to_datetime(c,format='%Y-%m-%d')
millis = str(round(time.time() * 1000))
current_timestamp = time.time()
   
#image01 = Image.open('pixabay300x256.png')
#image02 = Image.open('act_logo300x200.png')
#st.sidebar.image(image01, width=300, caption='Envio automático de e-mail') 
Titulo_Laterial = '<p style="font-weight: bolder; color:black; font-size: 32px;">Enviar Tarefas ao Quadro Trello</p>'
st.markdown(Titulo_Laterial, unsafe_allow_html=True)
mystyle1 =   '''<style> p{text-align:center;}</style>'''
st.markdown(mystyle1, unsafe_allow_html=True)
#st.sidebar.image(image02, width=300, caption='Desenvolvedor: Massaki de O. Igarashi') 

CON = sq.connect('Disciplinas.db')
cc = CON.cursor()
cc.execute(""" SELECT * from DISCIPLINAS """)
DB = cc.fetchall()
clean_db = pd.DataFrame(DB, columns=["ID","DISCIPLINA"])
#st.dataframe(clean_db)  

def Cadastrar_Tarefa(ID, USER, DISC, DataEntrega, Tarefa):
    connT = sqlite3.connect('Tarefas.db')
    cursorT = connT.cursor()
    cursorT.execute('''CREATE TABLE IF NOT EXISTS Tarefas(ID INT PRIMARY KEY NOT NULL,
                                                        USUARIO    TEXT NOT NULL,
                                                        DISCIPLINA TEXT NOT NULL,
                                                        D_ENTREGA  TEXT NOT NULL,
                                                        TAREFA     TEXT NOT NULL);''')
    connT.execute("""INSERT INTO Tarefas (ID,USUARIO,DISCIPLINA,D_ENTREGA,TAREFA) VALUES(?,?,?,?,?)""", (ID, USER, DISC, DataEntrega, Tarefa))
    connT.commit()
    st.write("Dados salvos com sucesso!")
    connT.close()
    
def exibir_tarefa():
    conn = sqlite3.connect('Tarefas.db')
    cursor = conn.execute(""" SELECT * FROM Tarefas""")
    rows = cursor.fetchall()
    for row in cursor:
       st.write("ID: ", row[0])
       st.write("Usuário: ", row[1])
       st.write("Diciplina: ", row[2])
       st.write("Data Entrega: ", row[3])
       st.write("Tarefa: ", row[4])
    if len(rows) != 0:
        db = pd.DataFrame(rows)    
        db.columns = ['ID' , 'USUÁRIO' , 'DISCIPLINA', 'Data Entrega' , 'TAREFA']
        st.dataframe(db)
    conn.close()

def main():
    col0, col1, col2 = st.columns(3)       
    with col0:
        st.page_link("https://gestaodetarefas.streamlit.app/Cadastrar_Disciplinas", label="Cadastrar disciplinas", icon="📃")
    with col1:
        st.page_link("https://gestaodetarefas.streamlit.app/Cadastrar_Usuario", label="Cadastrar Usuários", icon="👨‍💼")
    with col2:
        st.page_link("https://gestaodetarefas.streamlit.app/Painel_Tarefas", label="Painel de Tarefas", icon="📊") 
    MAIL =  st.sidebar.text_input("e-mail:")
    SENHA = st.sidebar.text_input("SENHA:")
    LOGAR = st.sidebar.button(label = '✔️ LOGAR') 
    MAIL2BOARD = ""
    conn = sqlite3.connect('Usuario.db') 
    cc = conn.cursor()
    cc.execute('SELECT * from USUARIO where MAIL=? and SENHA=?',(MAIL, SENHA))
	#ou
    #cursor = conn.execute("SELECT * from USUARIO where MAIL=? and SENHA=?", [MAIL, SENHA])
    cursor = cc.fetchall()
    for row in cursor:
        #IDuser = row[0]           
        #txtMAIL = str(st.text_input("e-mail: ", row[1]))
        MAIL2BOARD = st.sidebar.text_input("e-mail para Board Trello: ", row[2])   
    
    DISCIPLINA = st.selectbox("Selecione a Disciplina",clean_db["DISCIPLINA"],
                              #placeholder="Selecione a Disciplina a qual se refere a tafrefa!"
                              )
    #DISCIPLINA = st.selectbox("Selecione a Disciplina",
    #                        ("Arte", "Ciências", "Geografia", "Ling. Inglesa", "Matemática", "Matemática(Maker)", "Português", "Português/Ativs. Suplementares"),
    #                        #placeholder="Selecione a Disciplina a qual se refere a tafrefa!"
    #                        )
    DataEntrega = st.text_input("Data de Entrega: ", str(D.day) + "/" + str(D.month) + "/" + str(D.year))
    MSG = " "
    m = st.text_area("Digite a tarefa aqui: ", "\n ")
    if m is not None:
        textsplit = m.splitlines()
        for x in textsplit:
            MSG+=x + " \n "       
    FROM = "massaki.igarashi@gmail.com"
    #TO = st.text_input("seu e-mail cadastrado e-mail: ", "prof.massaki@gmail.com")
    if st.button(label = '✔️ ENVIAR'):                           
        ASSUNTO = DISCIPLINA + " (Para: " + DataEntrega + ")" 
        Cadastrar_Tarefa(current_timestamp, MAIL, DISCIPLINA, DataEntrega, MSG)
        exibir_tarefa()
        if MAIL2BOARD =="":
            st.write("Usuário não cadastrado! Não é possível enviar tarefa!")
        else:
            st.write(Send2Mail(FROM, MAIL2BOARD, ASSUNTO, MSG))
            http = urllib3.PoolManager()
            link = "https://docs.google.com/forms/d/e/1FAIpQLSf8vMlVulpPEPsoZDiXMV35qtiI0mjcxdyRjWQKNipc18F_AA/formResponse?&submit=Submit?usp=pp_url&entry.2053247179=" + DISCIPLINA + "&entry.1049878361=" + MSG + "&entry.1784768064=" + DataEntrega
            r = http.request('GET', link)
            r.status

    st.divider()
    Rodape = '<p style="font-weight: bolder; color:DarkBlue; font-size: 16px;">Desenvolvido por Massaki de O. Igarashi</p>'
    st.markdown(Rodape, unsafe_allow_html=True)
    mystyle1 =   '''<style> p{text-align:center;}</style>'''
    st.markdown(mystyle1, unsafe_allow_html=True)
if __name__ == '__main__':
	main()
