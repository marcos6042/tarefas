
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

    col1, col2, col3 = st.columns(3)

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
        st.header("✅ Tarefas")
        if st.button("Criar Nova Tarefa"):
            st.session_state.page = "Nova Tarefa"
        if st.button("Baixar Tarefa"):
            st.session_state.page = "Baixa de Tarefa"
    
    with col3:
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
    "Cadastro Filial": ["Empresa (Razão Social)", "CNPJ", "Município", "UF", "Tipo", "Inscrição Estadual", "Senha Sefaz", "filiais"],
    "Cadastro Setor": ["Nome do Setor", "setores"],
    "Cadastro Categoria": ["Nome da Categoria", "categorias"],
    "Cadastro Subcategoria": ["Categoria (Nome da Categoria)", "Nome da Subcategoria", "Periodicidade (Mensal, Trimestral, Anual, Avulso)", "subcategorias"],
    "Cadastro Usuário": ["Nome do Usuário", "E-mail", "usuarios"],
    "Nova Tarefa": ["Filial", "Setor", "Subcategoria", "Nome da Tarefa", "Competência (MM/AAAA)", "Vencimento", "Usuário (Múltipla Escolha)", "tarefas"]
}

if st.session_state.page in paginas:
    st.container()
    campos = paginas[st.session_state.page][:-1]
    lista = paginas[st.session_state.page][-1]
    st.subheader(st.session_state.page)
    
    if st.session_state.page == "Nova Tarefa":
        filiais_existentes = [f"{filial['Empresa (Razão Social)']} - {filial['UF']}" for filial in st.session_state.filiais]
        setores_existentes = [setor["Nome do Setor"] for setor in st.session_state.setores]
        usuarios_existentes = [usuario["Nome do Usuário"] for usuario in st.session_state.usuarios]
        
        dados = {
            "Filial": st.selectbox("Filial", filiais_existentes) if filiais_existentes else "Nenhuma filial cadastrada",
            "Setor": st.selectbox("Setor", setores_existentes) if setores_existentes else "Nenhum setor cadastrado",
            "Subcategoria": st.text_input("Subcategoria"),
            "Nome da Tarefa": st.text_input("Nome da Tarefa"),
            "Competência (MM/AAAA)": st.text_input("Competência", placeholder="MM/AAAA"),
            "Vencimento": st.date_input("Vencimento"),
            "Usuário (Múltipla Escolha)": st.multiselect("Usuário", usuarios_existentes) if usuarios_existentes else "Nenhum usuário cadastrado"
        }
    else:
        dados = {campo: st.text_input(campo) for campo in campos}
    
    if st.button("Salvar"):
        getattr(st.session_state, lista).append(dados)
        st.success(f"{st.session_state.page} cadastrada com sucesso!")
        st.rerun()
    
    df = pd.DataFrame(getattr(st.session_state, lista))
    if not df.empty:
        st.write(df)  # Exibição mais robusta e sem erros para a relação de cadastros
    
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.rerun()
