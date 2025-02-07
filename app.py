import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Gestão de Tarefas - Grupo Rodoxisto", layout="wide")

# Exibir logo
st.image("logo.jpeg", width=300)

st.title("Gestão de Tarefas - Grupo Rodoxisto")

# Controle de Navegação
if "page" not in st.session_state:
    st.session_state.page = "menu"

# Tela Principal
if st.session_state.page == "menu":
    st.subheader("Menu Principal")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.header("📂 Cadastros")
        if st.button("Cadastrar Empresa"):
            st.session_state.page = "Cadastro Empresa"
        if st.button("Cadastrar Filial"):
            st.session_state.page = "Cadastro Filial"
        if st.button("Cadastrar Setor"):
            st.session_state.page = "Cadastro Setor"
        if st.button("Cadastrar Categoria"):
            st.session_state.page = "Cadastro Categoria"
        if st.button("Cadastrar Subcategoria"):
            st.session_state.page = "Cadastro Subcategoria"
        if st.button("Cadastrar Usuário"):
            st.session_state.page = "Cadastro Usuário"

    with col2:
        st.header("📑 CND")
        if st.button("Consultar CND Federal"):
            st.session_state.page = "Consultar CND Federal"
        if st.button("Consultar CND Estadual"):
            st.session_state.page = "Consultar CND Estadual"
        if st.button("Emitir CRF Caixa"):
            st.session_state.page = "Emitir CRF Caixa"

    with col3:
        st.header("✅ Tarefas")
        if st.button("Criar Nova Tarefa"):
            st.session_state.page = "Nova Tarefa"
        if st.button("Baixar Tarefa"):
            st.session_state.page = "Baixa de Tarefa"

    with col4:
        st.header("📊 Relatórios")
        if st.button("Visualizar Kanban"):
            st.session_state.page = "Kanban"
        if st.button("Visualizar Calendário"):
            st.session_state.page = "Calendário"
        if st.button("Visualizar Lista"):
            st.session_state.page = "Lista"

# Criando o arquivo para download
with open(file_path, "w") as file:
    file.write(codigo)

# Retornando o caminho do arquivo para download
file_path
