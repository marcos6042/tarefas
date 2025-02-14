
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Gestão de Tarefas - Grupo Rodoxisto", layout="wide")

# Exibir logo
st.image("logo.jpeg", width=300)

st.title("Gestão de Tarefas - Grupo Rodoxisto")

# Controle de Navegação
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "empresas" not in st.session_state:
    st.session_state.empresas = []
if "filiais" not in st.session_state:
    st.session_state.filiais = []
if "setores" not in st.session_state:
    st.session_state.setores = []
if "categorias" not in st.session_state:
    st.session_state.categorias = []
if "subcategorias" not in st.session_state:
    st.session_state.subcategorias = []
if "usuarios" not in st.session_state:
    st.session_state.usuarios = []
if "tarefas" not in st.session_state:
    st.session_state.tarefas = []

# Tela Principal
if st.session_state.page == "menu":
    st.subheader("Menu Principal")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Visualizar Kanban"):
            st.session_state.page = "Kanban"
            st.rerun()

if st.session_state.page == "Kanban":
    st.subheader("Quadro Kanban")
    
    col1, col2, col3, col4 = st.columns(4)
    
    categorias = {
        "À Vencer": [],
        "Atrasado": [],
        "Entregue no Prazo": [],
        "Entregue em Atraso": []
    }
    
    hoje = datetime.today().date()
    
    for tarefa in st.session_state.tarefas:
        vencimento = tarefa.get("Vencimento")
        baixa = tarefa.get("Baixa", False)
        if isinstance(vencimento, str):
            try:
                vencimento = datetime.strptime(vencimento, "%Y-%m-%d").date()
            except ValueError:
                continue
        
        if vencimento:
            if not baixa:
                if vencimento >= hoje:
                    categorias["À Vencer"].append(tarefa)
                else:
                    categorias["Atrasado"].append(tarefa)
            else:
                if vencimento >= hoje:
                    categorias["Entregue no Prazo"].append(tarefa)
                else:
                    categorias["Entregue em Atraso"].append(tarefa)
    
    with col1:
        st.subheader("À Vencer")
        for t in categorias["À Vencer"]:
            st.write(f"{t.get('Nome da Tarefa', 'Sem Nome')}")
    
    with col2:
        st.subheader("Atrasado")
        for t in categorias["Atrasado"]:
            st.write(f"{t.get('Nome da Tarefa', 'Sem Nome')}")
    
    with col3:
        st.subheader("Entregue no Prazo")
        for t in categorias["Entregue no Prazo"]:
            st.write(f"{t.get('Nome da Tarefa', 'Sem Nome')}")
    
    with col4:
        st.subheader("Entregue em Atraso")
        for t in categorias["Entregue em Atraso"]:
            st.write(f"{t.get('Nome da Tarefa', 'Sem Nome')}")
    
    # Criando gráficos
    status_counts = {key: len(value) for key, value in categorias.items()}
    
    st.subheader("Gráficos de Tarefas")
    
    if any(status_counts.values()):
        fig, ax = plt.subplots()
        ax.bar(status_counts.keys(), status_counts.values())
        ax.set_ylabel("Quantidade de Tarefas")
        ax.set_title("Distribuição das Tarefas no Kanban")
        st.pyplot(fig)
        
        fig, ax = plt.subplots()
        ax.pie(status_counts.values(), labels=status_counts.keys(), autopct='%1.1f%%', startangle=90)
        ax.set_title("Proporção das Tarefas no Kanban")
        st.pyplot(fig)
    else:
        st.write("Nenhuma tarefa cadastrada para exibir nos gráficos.")
