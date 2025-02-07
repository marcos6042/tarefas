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

# Página de Solicitação de CND Estadual
if st.session_state.page == "Consultar CND Estadual":
    st.subheader("Solicitação de CND Estadual")
    filiais = [(f["Empresa"], f["UF"]) for f in st.session_state.filiais]
    selecao_filiais = st.multiselect("Selecione as Filiais", filiais, format_func=lambda x: f"{x[0]} - {x[1]}")
    
    if st.button("Solicitar CND Estadual"):
        for empresa, uf in selecao_filiais:
            cnpj = next((f["CNPJ"] for f in st.session_state.filiais if f["Empresa"] == empresa and f["UF"] == uf), None)
            if cnpj:
                url = f"http://www.cdw.fazenda.{uf.lower()}.gov.br/cdw/emissao/certidaoAutomatica"
                response = requests.post(url, data={"cnpj": cnpj})
                if response.status_code == 200:
                    with open(f"CND_{empresa}_{uf}.pdf", "wb") as file:
                        file.write(response.content)
                    st.success(f"CND Estadual da {empresa} ({uf}) armazenada com sucesso!")
                else:
                    st.error(f"Erro ao solicitar CND Estadual da {empresa} ({uf})")
    
    if st.button("Voltar"):
        st.session_state.page = "menu"
        st.experimental_rerun()
