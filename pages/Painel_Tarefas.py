import streamlit as st
import sqlite3
import requests
import urllib3
from io import BytesIO
from urllib3 import request
import pandas as pd

import datetime
from datetime import datetime
from datetime import date
import pytz
import time

from gtts import gTTS #Lib para Conversão Text2Voice. Em seguida pode usar Gemini para converter voice para texto
#NLP Package
from enelvo.normaliser import Normaliser
norm = Normaliser(tokenizer='readable')

datetime_br= datetime.now(pytz.timezone('America/Sao_Paulo'))
#t = datetime_br.strftime('%d:%m:%Y %H:%M:%S %Z %z')
current_time = datetime_br.strftime('%d/%m/%Y %H:%M')
c = datetime.now()
D = pd.to_datetime(c,format='%Y-%m-%d')
c = datetime.now()
H = pd.to_datetime(c,format='%Y-%m-%d')
if H.month <10:
  Hoje = str(H.day) + "/0" + str(H.month) + "/" + str(H.year)
  #MES = "0" + str(D.month)
else:
  Hoje = str(H.day) + "/" + str(H.month) + "/" + str(H.year)

MES = D.month


import matplotlib.pyplot as plt
#https://discuss.streamlit.io/t/how-to-draw-pie-chart-with-matplotlib-pyplot/13967/2

# Page setting
st.set_page_config(layout="wide", page_title="Gestão de TAREFAS")
  
def DB_FiltraMES2(db, MES, DataHoje):
    selecao2 = db['DATA_ENTREGA']==DataHoje
    dbHJ = db[selecao2]
    format = '%d/%m/%Y'
    Dentrega = pd.to_datetime(db['DATA_ENTREGA'], format = format)
    pos = 0 #pos garante que seja inserido novo tempo na Tupla Tabela a partir da posição 0
    Tabela = {'DISCIPLINA': [' '], 'TAREFA': [' '], 'DATA_ENTREGA':[' '], 'USUARIO':[' ']}
    TarefasDeHoje=[]
    for i in range(len(Dentrega)):
        #A subrotina a seguir é para filtrar e adicionar no vetor TarefasDeHoje todas as tarefas com a entrega hoje
        #Depois será retornado num DataFrame junto com o DataFrame filtrado
        Data = str(Dentrega[i].day) + "/" + str(Dentrega[i].month) + "/" + str(Dentrega[i].year)
        
        if Data== Hoje: 
            TarefasDeHoje.append(db['TAREFA'][i])
            
        #A rotina a seguir irácriar o DataFRame dos dados filtrados referente ao mês escolhido para exibição dos gráficos
        if Dentrega[i].month==MES:
            if pos == 0:
                Tabela['DISCIPLINA'][pos] = db['DISCIPLINA'][i]
                Tabela['TAREFA'][pos] = db['TAREFA'][i]
                Tabela['DATA_ENTREGA'][pos] = Dentrega[i]
                Tabela['USUARIO'][pos] = db['USUARIO'][i]
                pos += 1
            else:
                Tabela['DISCIPLINA'].append(db['DISCIPLINA'][i])
                Tabela['TAREFA'].append(db['TAREFA'][i])
                Tabela['DATA_ENTREGA'].append(Dentrega[i])
                Tabela['USUARIO'].append(db['USUARIO'][i])
                pos += 1
    df = (pd.DataFrame(Tabela)).dropna()
    return df, dbHJ
def NPL_and_Text2Voice(dbTarefasDeHoje):    
    dbTarefasDeHoje.columns = ['DISCIPLINA', 'TAREFA', 'DATA_ENTREGA', 'USUARIO'] 
    ListaTarefas = []
    for c in range(len(dbTarefasDeHoje)):
        ListaTarefas.append(norm.normalise(str(dbTarefasDeHoje['TAREFA'][c])))
    
    TextoSLTBox = 'Tarefas de Hoje (' + str(Hoje) + ")"
    coluna0, coluna1 = st.columns(2)      
    with coluna0:
        st.subheader(" ")
        option = st.selectbox(TextoSLTBox, ListaTarefas)
    with coluna1:    
        if option:
            msg = "Consta como sua tarefa de hoje, " + str(Hoje) + " " + option
            language = 'pt'     # Language in which you want to convert
            # Passing the text and language to the engine,here we have marked slow=False. Which tells the module that the converted audio should have a high speed
            myobj1 = gTTS(text= msg, lang=language, slow=False)
            nameAudio = "audio.mp3"
            myobj1.save(nameAudio)   #Saving the converted audio in a mp3 file
            # Playing the converted file
            st.write("Clique play p/ escutar a tarefa")
            audio_file = open(nameAudio, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/ogg',start_time=0)
    
def Grafico_Pizza(Rotulos, Quantias, Legenda, posExplode, LocLEG):
    # Rotulos: etiquetamento dos dados
    # Quantias: dados numéricos referente a cada rótulo
    # Legenda: etiquetamento da legenda
    # posExplode: posição na qual se encontra a fatia da pizza que se deseja ressaltar (explodir)
    # LocLEG: Localização onde será posicionada a Legenda do Gráfico (Ref: https://www.geeksforgeeks.org/change-the-legend-position-in-matplotlib/)    
    
    fig, ax = plt.subplots()
    explode = []
    for i in range(len(Rotulos)):
        if i !=posExplode:
            explode.append(0)
        else:
            explode.append(0.1)    
    ax.pie(Quantias, 
        explode=explode, 
        labels=Legenda, 
        autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.legend(title='Disciplinas',
            loc=LocLEG,
            bbox_to_anchor=(1, 0, 0.5, 1))
    st.pyplot(fig)

def Grafico_Barra_Mono(Rotulos, Quantias, Legenda):
    #A fazer: mudar conceito para declaracao classes e colocar objetos nos títulos dos eixos para facilitar uso da função
    fig, ax = plt.subplots()
    ax.bar(Rotulos, Quantias, label=Legenda)
    ax.set_ylabel('QTD de tarefas por Disciplina')
    ax.set_title('Tarefas por Disciplina')
    ax.legend(title = 'Disciplinas')
    st.pyplot(fig)

def Mes2Num(NomeMes):
    if NomeMes == 'Janeiro':
        return 1
    if NomeMes == 'Fevereiro':
        return 2
    if NomeMes == 'Março':
        return 3
    if NomeMes == 'Abril':
        return 4
    if NomeMes == 'Maio':
        return 5
    if NomeMes == 'Junho':
        return 6
    if NomeMes == 'Julho':
        return 7
    if NomeMes == 'Agosto': 
        return 8
    if NomeMes == 'Setembro':
        return 9
    if NomeMes == 'Outubro': 
        return 10
    if NomeMes == 'Novembro': 
        return 11
    if NomeMes == 'Dezembro':
        return 12

def main():         
    col0, col1, col2 = st.columns(3)       
    with col0:
        st.page_link("Cadastrar_Tarefas.py", label="Cadastrar Tarefas", icon="📌") 
    with col1:
        st.page_link("pages/Cadastrar_Disciplinas.py", label="Cadastrar disciplinas", icon="📃")
    with col2:
        st.page_link("pages/Cadastrar_Usuario.py", label="Cadastrar Usuários", icon="👨‍💼")

    #USER =  st.sidebar.text_input("e-mail:", "massaki.igarashi@gmail.com")
    #SENHA = st.sidebar.text_input("SENHA:", "84971")
    USER =  st.sidebar.text_input("e-mail:")
    SENHA = st.sidebar.text_input("SENHA:")
    LOGAR = st.sidebar.button(label = '✔️ LOGAR') 
    MAIL2BOARD = ""
    conn = sqlite3.connect('Usuario.db') 
    cc = conn.cursor()
    cc.execute('SELECT * from USUARIO where MAIL=? and SENHA=?',(USER, SENHA))
	#ou
    #cursor = conn.execute("SELECT * from USUARIO where MAIL=? and SENHA=?", [MAIL, SENHA])
    cursor = cc.fetchall()
    for row in cursor:
        #IDuser = row[0]           
        #txtMAIL = str(st.text_input("e-mail: ", row[1]))
        MAIL2BOARD = st.sidebar.text_input("e-mail para Board Trello: ", row[2]) 
    conn.close()
    
    
    MesSelecionado = st.sidebar.selectbox('Selecione o mês a consultar',
                            ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'),
                            index=int(MES)-1)    
    NumMes = Mes2Num(MesSelecionado)
    #CSV
    urlCSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSl_OAa9Xv81pQ9edrGF_RgoBwI78BEeuhGplXTFAX7CayaL9nwZOITQUxLQ2Ggl21HUeeTfqkU8xHw/pub?gid=283390209&single=true&output=csv"
    rD = requests.get(urlCSV)
    dataD = rD.content
    db = pd.read_csv(BytesIO(dataD), index_col=0)
    NregD = len(db)
    db.columns = ['DISCIPLINA', 'TAREFA', 'DATA_ENTREGA', 'USUARIO']
    selecao = db['USUARIO']==USER
    db = db[selecao]              
    #dblimpo = db.dropna() #Limpa dados vazios
    TimeStamp = db.index  
    df, DBTarefasDeHoje = DB_FiltraMES2(db, MES, Hoje)
    #df é do DataFrame FILTRADO
        
    if df['DISCIPLINA'][0] != " ":
        resp = True
    else:
        resp = False
    
    if resp:
        resumoDISC = df['DISCIPLINA'].value_counts()
        DBresumoDISC = pd.DataFrame(resumoDISC)
        n = len(resumoDISC)
        VetLabels = []
        for i in range(n):
            texto = str(resumoDISC.index[i]) + ", " + str(DBresumoDISC['count'][i])
            VetLabels.append(texto)
        labels = VetLabels
        #A rotina a seguir serve para criar um novo vetor labels2 que armazenará apenas as 3 primeiras letras de cada Disciplina
        labels2 = []
        for k in range(0, len(labels)):
            labels2.append(str(labels[k])[0:4])
           
        sizes =  DBresumoDISC['count']
        IndicadorTarefas = round(sizes.sum()/len(labels), 1)
        mystyle1 =   '''<style> p{text-align:left;}</style>'''
        st.markdown(mystyle1, unsafe_allow_html=True)
        colA, colB = st.columns(2)      
        with colA:
            st.title(" ")
            Titulo = '<p style="font-weight: bolder; color:black; font-size: 48px;">Web app Gestão de Tarefas</p>'
            st.markdown(Titulo, unsafe_allow_html=True)
            mystyle1 =   '''<style> p{text-align:left;}</style>'''
            st.markdown(mystyle1, unsafe_allow_html=True) 
        with colB:
            st.subheader("")
            NPL_and_Text2Voice(DBTarefasDeHoje)
            
        tab1, tab2 = st.tabs(["Gráficos", "Dados"])
        with tab1:   
            col_1, col_2, col_3 = st.columns(3) 
            with col_1:
                #st.title("INDICADOR")
                st.metric("Tarefas/Disciplina:", IndicadorTarefas)
            with col_2:
                MAIOR = 'MAIOR nº de Tarefas: \n' + str(resumoDISC.index[0]) 
                menor = 'menor nº de Tarefas: \n' + str(resumoDISC.index[len(resumoDISC)-1])           
                #st.title("MAIOR E MENOR Nº DE TAREFAS")
                #st.title(MAIOR)
                TEXTO1 = '<p style="font-family:tahoma; color:darkblue; text-align: left; font-size: 22px;"> %s </p>' % MAIOR
                st.markdown(TEXTO1, unsafe_allow_html=True)
            with col_3:
                TEXTO2 = '<p style="font-family:tahoma; color:darkblue; text-align: left; font-size: 20px;"> %s </p>' % menor
                st.markdown(TEXTO2, unsafe_allow_html=True) 
            
            
            colD, colE = st.columns(2)       
            with colD:
                Grafico_Barra_Mono(labels2, sizes, labels)
            with colE:
                Grafico_Pizza(labels, sizes, labels, 0, "upper left")     
        with tab2:  
            st.dataframe(df.head(5))
    else:
        Mensagem = '<p style="font-weight: bolder; color:blue; font-size: 56px;">Não há dados disponíveis para o mês selecionado!</p>'
        st.markdown(Mensagem, unsafe_allow_html=True)
        mystyle1 =   '''<style> p{text-align:left;}</style>'''
        st.markdown(mystyle1, unsafe_allow_html=True)
    
    st.divider()
    
    Rodape = '<p style="font-weight: bolder; color:DarkBlue; font-size: 16px;">Desenv. por Massaki de O. Igarashi</p>'
    st.sidebar.markdown(Rodape, unsafe_allow_html=True)
    mystyle1 =   '''<style> p{text-align:center;}</style>'''
    st.sidebar.markdown(mystyle1, unsafe_allow_html=True)
    
if __name__ == '__main__':
	main()
