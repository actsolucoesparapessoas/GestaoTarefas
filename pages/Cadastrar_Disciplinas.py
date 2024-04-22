# myFirstStreamlitApp.py
#import the libraries
import streamlit as st
import sqlite3
import pandas as pd
import time
import pandas as pd

def exibir():
    conn = sqlite3.connect('Disciplinas.db')
    cursor = conn.execute(""" SELECT * from DISCIPLINAS """)
    rows = cursor.fetchall()
    for row in cursor:
       st.write("ID: ", row[0])
       st.write("DISCIPLINA: ", row[1])
  
    if len(rows) != 0:
        db = pd.DataFrame(rows)    
        db.columns = ['ID' , 'DISCIPLINA']
        st.dataframe(db)
    conn.close()
    

def inicializar():
    #1º)Para criar um banco de dados SQL , usamos o seguinte comando:
    conn = sqlite3.connect('Disciplinas.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS DISCIPLINAS(ID INT PRIMARY KEY     NOT NULL,
                                                            DISCIPLINA TEXT NOT NULL);''')
    conn.close()

    #2º)INSERT data and READ this data
    #   Following Python program shows how to create records in the COMPANY table created in the above example.
    conn = sqlite3.connect('Disciplinas.db')
    cursor = conn.execute(""" SELECT * from DISCIPLINAS """)
    rows = cursor.fetchall()
    n = len(rows)
    return n

col0, col1, col2 = st.columns(3)       
with col0:
    st.page_link("https://ctrltarefas.streamlit.app/", label="Cadastrar Tarefas", icon="📌") 
with col1:
    st.page_link("https://ctrltarefas.streamlit.app/Cadastrar_Usuario", label="Cadastrar Usuários", icon="👨‍💼")
with col2:
    st.page_link("https://ctrltarefas.streamlit.app/Painel_Tarefas", label="Painel de Tarefas", icon="📊") 

tab1, tab2 = st.tabs(["Cadastrar", "EXIBIR"])
with tab1:    
    n = inicializar()    
    ID = str(n+1)
    form = st.empty()
    txtDISCIPLINA = form.text_input("Disciplina:", value="", key="1")
    if txtDISCIPLINA:
        if st.button('Salvar'):
            conn = sqlite3.connect('Disciplinas.db')
            cursor = conn.cursor()
            conn.execute("""INSERT INTO DISCIPLINAS (ID, DISCIPLINA) \
                            VALUES (?,?)
                            """, (ID, txtDISCIPLINA))
            conn.commit()
            st.write("Registros Salvos com sucesso!")      
            n = inicializar()
            ID = str(n+1)
            txtDISCIPLINA = form.text_input("Disciplina:", value="", key="2")
            st.divider()
            st.write("Bem vinda(o) ao TASK_TRELLO! Acesse seu e-mail cadastrado para obter a senha de acesso.")        
with tab2: 
    exibir()
