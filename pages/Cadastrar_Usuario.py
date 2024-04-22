# myFirstStreamlitApp.py
#import the libraries
import streamlit as st
import sqlite3
import pandas as pd
import time
import pandas as pd
import numpy as np
import random  # necessário para utilizar o módulo random
from Send2MaillMSK import Send2Mail

# Page setting
st.set_page_config(layout="wide", page_title="Gestão de TAREFAS")
  
vet = str(np.zeros(4))
def exibir():
    conn = sqlite3.connect('Usuario.db')
    cursor = conn.execute(""" SELECT * FROM USUARIO """)
    rows = cursor.fetchall()
    for row in cursor:
       st.write("ID: ", row[0])
       st.write("MAIL: ", row[1])
       st.write("MAIL2BOARD: ", row[2])
       st.write("SENHA: ", row[3])   
    if len(rows) != 0:
        db = pd.DataFrame(rows)    
        db.columns = ['ID' , 'MAIL' , 'MAIL2BOARD', 'SENHA']
        st.dataframe(db)
    conn.close()

#1º)Para criar um banco de dados SQL , usamos o seguinte comando:
conn = sqlite3.connect('Usuario.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS USUARIO(ID INT PRIMARY KEY     NOT NULL,
                                                    MAIL            TEXT    NOT NULL,
                                                    MAIL2BOARD      TEXT    NOT NULL,
                                                    SENHA      TEXT    NOT NULL);''')
conn.close()

#2º)INSERT data and READ this data
#   Following Python program shows how to create records in the COMPANY table created in the above example.
conn = sqlite3.connect('Usuario.db')
cursor = conn.execute(""" SELECT * FROM USUARIO """)
rows = cursor.fetchall()
n = len(rows)


col0, col1, col2 = st.columns(3)       
with col0:
    st.page_link("https://gestaodetarefas.streamlit.app/", label="Cadastrar Tarefas", icon="📌") 
with col1:
    st.page_link("https://gestaodetarefas.streamlit.app/Cadastrar_Disciplinas", label="Cadastrar Disciplinas", icon="📃")
with col2:
    st.page_link("https://gestaodetarefas.streamlit.app/Painel_Tarefas", label="Painel de Tarefas", icon="📊") 
 
tab1, tab2 = st.tabs(["Cadastrar", "EXIBIR"])
with tab1:
    txtID = str(n+1)
    txtMAIL = st.text_input("Seu e-mail:")
    txtMAIL2BOARD = st.text_input("e-mail para Board Trello")
    random.seed()
    numeros = random.getstate()
    sorteio = random.sample(range(10), k=5)
    senha = str(sorteio[0])+str(sorteio[1])+str(sorteio[2])+str(sorteio[3])+str(sorteio[4])
    #txtSENHA = st.text_input("SENHA: ", senha)

    if st.button('Salvar'):
        conn.execute("""INSERT INTO USUARIO (ID, MAIL, MAIL2BOARD, SENHA) \
                        VALUES (?,?,?,?)
                        """, (txtID, txtMAIL, txtMAIL2BOARD, senha))
        conn.commit()
        st.write("Records created successfully")        
        st.write(Send2Mail("massaki.igarashi@gmail.com", txtMAIL, "Bem vindo(a) ao TASK_TRELLO - A seguir sua senha de acesso, guarde-a!", "Para acessar a plataforma digite este e-mail cadastrado mais a senha de acesso: "+ senha))
        st.divider()
        st.write("Bem vinda(o) ao TASK_TRELLO! Acesse seu e-mail cadastrado para obter a senha de acesso.")        
with tab2: 
    st.write("")
    #exibir()
