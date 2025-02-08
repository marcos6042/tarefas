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
if st.session_state.page == "Cadastro Empresa":
    st.subheader("Cadastro de Empresa")
    razao_social = st.text_input("Razão Social")
    cnpj = st.text_input("CNPJ")
    if st.button("Salvar"):
        st.session_state.empresas.append({"Razão Social": razao_social, "CNPJ": cnpj})
        st.success("Empresa cadastrada com sucesso!")
    if st.button("Excluir"):
        st.session_state.empresas = []
        st.success("Cadastro excluído!")
    if st.button("Atualizar"):
        st.experimental_rerun()
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.experimental_rerun()

if st.session_state.page == "Cadastro Filial":
    st.subheader("Cadastro de Filial")
    empresa = st.selectbox("Empresa", [e["Razão Social"] for e in st.session_state.empresas] if st.session_state.empresas else ["Nenhuma empresa cadastrada"])
    cnpj = st.text_input("CNPJ")
    tipo = st.selectbox("Tipo", ["Matriz", "Filial"])
    municipio = st.text_input("Município")
    uf = st.selectbox("UF", ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
    if st.button("Salvar"):
        st.session_state.filiais.append({"Empresa": empresa, "CNPJ": cnpj, "Tipo": tipo, "Município": municipio, "UF": uf})
        st.success("Filial cadastrada com sucesso!")
    if st.button("Excluir"):
        st.session_state.filiais = []
        st.success("Cadastro excluído!")
    if st.button("Atualizar"):
        st.experimental_rerun()
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.experimental_rerun()

if st.session_state.page == "Cadastro Setor":
    st.subheader("Cadastro de Setor")
    nome_setor = st.text_input("Nome do Setor")
    if st.button("Salvar"):
        st.session_state.setores.append({"Nome": nome_setor})
        st.success("Setor cadastrado com sucesso!")
    if st.button("Excluir"):
        st.session_state.setores = []
        st.success("Cadastro excluído!")
    if st.button("Atualizar"):
        st.experimental_rerun()
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.experimental_rerun()

if st.session_state.page == "Cadastro Categoria":
    st.subheader("Cadastro de Categoria")
    nome_categoria = st.text_input("Nome da Categoria")
    if st.button("Salvar"):
        st.session_state.categorias.append({"Nome": nome_categoria})
        st.success("Categoria cadastrada com sucesso!")
    if st.button("Excluir"):
        st.session_state.categorias = []
        st.success("Cadastro excluído!")
    if st.button("Atualizar"):
        st.experimental_rerun()
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.experimental_rerun()

if st.session_state.page == "Cadastro Subcategoria":
    st.subheader("Cadastro de Subcategoria")
    categoria = st.selectbox("Categoria", [c["Nome"] for c in st.session_state.categorias] if st.session_state.categorias else ["Nenhuma categoria cadastrada"])
    nome_subcategoria = st.text_input("Nome da Subcategoria")
    periodicidade = st.selectbox("Periodicidade", ["Mensal", "Trimestral", "Anual", "Avulso"])
    if st.button("Salvar"):
        st.session_state.subcategorias.append({"Categoria": categoria, "Nome": nome_subcategoria, "Periodicidade": periodicidade})
        st.success("Subcategoria cadastrada com sucesso!")
    if st.button("Excluir"):
        st.session_state.subcategorias = []
        st.success("Cadastro excluído!")
    if st.button("Atualizar"):
        st.experimental_rerun()
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.experimental_rerun()

if st.session_state.page == "Cadastro Usuário":
    st.subheader("Cadastro de Usuário")
    nome_usuario = st.text_input("Nome do Usuário")
    email = st.text_input("E-mail")
    if st.button("Salvar"):
        st.session_state.usuarios.append({"Nome": nome_usuario, "Email": email})
        st.success("Usuário cadastrado com sucesso!")
    if st.button("Excluir"):
        st.session_state.usuarios = []
        st.success("Cadastro excluído!")
    if st.button("Atualizar"):
        st.experimental_rerun()
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.experimental_rerun()
