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

# Página de Solicitação de CND Estadual
if st.session_state.page == "Consultar CND Estadual":
    st.subheader("Solicitação de CND Estadual")
    filiais = [("Empresa 1", "SP"), ("Empresa 2", "RJ"), ("Empresa 3", "MG")]  # Simulação de filiais cadastradas
    selecao_filiais = st.multiselect("Selecione as Filiais", filiais, format_func=lambda x: f"{x[0]} - {x[1]}")
    if st.button("Solicitar CND Estadual"):
        for empresa, uf in selecao_filiais:
            cnpj = "00000000000000"  # Simulação de CNPJ
            url = f"https://sefaz.{uf.lower()}.gov.br/api/cnd/{cnpj}"
            response = requests.get(url)
            if response.status_code == 200:
                with open(f"CND_{empresa}_{uf}.pdf", "wb") as file:
                    file.write(response.content)
                st.success(f"CND Estadual da {empresa} ({uf}) armazenada com sucesso!")
            else:
                st.error(f"Erro ao solicitar CND Estadual da {empresa} ({uf})")

# Páginas de Cadastro
if st.session_state.page == "Cadastro Empresa":
    st.subheader("Cadastro de Empresa")
    razao_social = st.text_input("Razão Social")
    cnpj = st.text_input("CNPJ")
    if st.button("Salvar"):
        st.success("Empresa cadastrada com sucesso!")

if st.session_state.page == "Cadastro Filial":
    st.subheader("Cadastro de Filial")
    empresa = st.selectbox("Empresa", ["Empresa 1", "Empresa 2", "Empresa 3"])  # Simulação de empresas cadastradas
    cnpj = st.text_input("CNPJ")
    tipo = st.selectbox("Tipo", ["Matriz", "Filial"])
    municipio = st.text_input("Município")
    uf = st.selectbox("UF", ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
    if st.button("Salvar"):
        st.success("Filial cadastrada com sucesso!")

if st.session_state.page == "Cadastro Setor":
    st.subheader("Cadastro de Setor")
    nome_setor = st.text_input("Nome do Setor")
    if st.button("Salvar"):
        st.success("Setor cadastrado com sucesso!")

if st.session_state.page == "Cadastro Categoria":
    st.subheader("Cadastro de Categoria")
    nome_categoria = st.text_input("Nome da Categoria")
    if st.button("Salvar"):
        st.success("Categoria cadastrada com sucesso!")

if st.session_state.page == "Cadastro Subcategoria":
    st.subheader("Cadastro de Subcategoria")
    categoria = st.selectbox("Categoria", ["Categoria 1", "Categoria 2", "Categoria 3"])  # Simulação de categorias cadastradas
    nome_subcategoria = st.text_input("Nome da Subcategoria")
    periodicidade = st.selectbox("Periodicidade", ["Mensal", "Trimestral", "Anual", "Avulso"])
    if st.button("Salvar"):
        st.success("Subcategoria cadastrada com sucesso!")

if st.session_state.page == "Cadastro Usuário":
    st.subheader("Cadastro de Usuário")
    nome_usuario = st.text_input("Nome do Usuário")
    email = st.text_input("E-mail")
    if st.button("Salvar"):
        st.success("Usuário cadastrado com sucesso!")
