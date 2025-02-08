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

# Páginas de Cadastro e Tarefas
paginas = {
    "Cadastro Empresa": ["Razão Social", "CNPJ", "empresas"],
    "Cadastro Filial": ["Empresa (Razão Social)", "CNPJ", "Tipo", "Município", "UF", "Inscrição Estadual", "Senha Sefaz", "filiais"],
    "Cadastro Setor": ["Nome do Setor", "setores"],
    "Cadastro Categoria": ["Nome da Categoria", "categorias"],
    "Cadastro Subcategoria": ["Categoria (Nome da Categoria)", "Nome da Subcategoria", "Periodicidade", "subcategorias"],
    "Cadastro Usuário": ["Nome do Usuário", "E-mail", "usuarios"]
}

if st.session_state.page in paginas:
    st.container()
    campos = paginas[st.session_state.page][:-1]
    lista = paginas[st.session_state.page][-1]
    st.subheader(st.session_state.page)
    
    if st.session_state.page == "Cadastro Filial":
        empresas_existentes = [empresa["Razão Social"] for empresa in st.session_state.empresas]
        dados = {"Empresa (Razão Social)": st.selectbox("Empresa", empresas_existentes) if empresas_existentes else "Nenhuma empresa cadastrada"}
    elif st.session_state.page == "Cadastro Subcategoria":
        categorias_existentes = [categoria["Nome da Categoria"] for categoria in st.session_state.categorias]
        dados = {"Categoria (Nome da Categoria)": st.selectbox("Categoria", categorias_existentes) if categorias_existentes else "Nenhuma categoria cadastrada"}
    else:
        dados = {campo: st.text_input(campo) for campo in campos}

    if st.button("Salvar"):
        getattr(st.session_state, lista).append(dados)
        st.success(f"{st.session_state.page} cadastrada com sucesso!")
        st.rerun()
    
    df = pd.DataFrame(getattr(st.session_state, lista))
    if not df.empty:
        for i, row in df.iterrows():
            col1, col2, col3 = st.columns([5, 1, 1])
            col1.write(row)
            if col2.button("✏️", key=f"edit_{lista}_{i}"):
                st.warning("Função de edição em desenvolvimento.")
            if col3.button("🗑️", key=f"del_{lista}_{i}"):
                getattr(st.session_state, lista).pop(i)
                st.success("Registro excluído com sucesso!")
                st.rerun()
    
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.rerun()
