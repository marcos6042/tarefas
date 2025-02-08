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
        if st.button("Consultar CND Estadual"):
            st.session_state.page = "Consultar CND Estadual"
    
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

# Páginas de Cadastro
if st.session_state.page == "Nova Tarefa":
    st.subheader("Nova Tarefa")
    filial = st.selectbox("Filial", [f["Empresa"] for f in st.session_state.filiais] if st.session_state.filiais else ["Nenhuma filial cadastrada"])
    setor = st.selectbox("Setor", [s["Nome"] for s in st.session_state.setores] if st.session_state.setores else ["Nenhum setor cadastrado"])
    subcategoria = st.selectbox("Subcategoria", [sc["Nome"] for sc in st.session_state.subcategorias] if st.session_state.subcategorias else ["Nenhuma subcategoria cadastrada"])
    nome_tarefa = st.text_input("Nome da Tarefa")
    competencia = st.date_input("Competência")
    vencimento = st.date_input("Vencimento")
    usuario = st.multiselect("Usuários", [u["Nome"] for u in st.session_state.usuarios] if st.session_state.usuarios else ["Nenhum usuário cadastrado"])
    if st.button("Salvar"):
        st.session_state.tarefas.append({"Filial": filial, "Setor": setor, "Subcategoria": subcategoria, "Nome": nome_tarefa, "Competência": competencia, "Vencimento": vencimento, "Usuário": usuario})
        st.success("Tarefa cadastrada com sucesso!")
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.experimental_rerun()

if st.session_state.page == "Baixa de Tarefa":
    st.subheader("Baixa de Tarefa")
    tarefa = st.selectbox("Selecionar Tarefa", [t["Nome"] for t in st.session_state.tarefas] if st.session_state.tarefas else ["Nenhuma tarefa cadastrada"])
    data_baixa = st.date_input("Data de Baixa")
    comprovante = st.file_uploader("Anexar Comprovante")
    if st.button("Baixar Tarefa"):
        st.success("Tarefa baixada com sucesso!")
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.experimental_rerun()

if st.session_state.page == "Kanban":
    st.subheader("Kanban de Tarefas")
    status_options = ["A Vencer", "Atraso", "Entregue no Prazo", "Entregue Fora do Prazo"]
    status = st.radio("Status", status_options)
    tarefas_filtradas = [t for t in st.session_state.tarefas if status in t.get("Status", "")]
    df = pd.DataFrame(tarefas_filtradas)
    st.write(df)
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.experimental_rerun()

if st.session_state.page == "Calendário":
    st.subheader("Calendário de Tarefas")
    df_calendar = pd.DataFrame(st.session_state.tarefas)
    st.write(df_calendar.sort_values(by="Vencimento"))
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.experimental_rerun()

if st.session_state.page == "Lista":
    st.subheader("Lista de Tarefas")
    df_list = pd.DataFrame(st.session_state.tarefas)
    st.write(df_list)
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.experimental_rerun()
