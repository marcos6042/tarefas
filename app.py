import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Gestão de Tarefas - Grupo Rodoxisto", layout="wide")

# Exibir logo
st.image("logo.jpeg", width=300)

st.title("Gestão de Tarefas - Grupo Rodoxisto")

# Sidebar para navegação
menu = st.sidebar.selectbox("Menu", ["Cadastro", "Tarefas", "Relatórios", "Configurações"])

# Simulação de banco de dados
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

# Cadastro
if menu == "Cadastro":
    cadastro_opcao = st.sidebar.selectbox("Opções", ["Empresa", "Filial", "Setor", "Categoria", "Subcategoria", "Usuário"])
    
    if cadastro_opcao == "Empresa":
        st.subheader("Cadastro de Empresa")
        razao_social = st.text_input("Razão Social")
        cnpj = st.text_input("CNPJ")
        if st.button("Salvar"):
            st.session_state.empresas.append({"Razão Social": razao_social, "CNPJ": cnpj})
            st.success("Empresa cadastrada com sucesso!")

    elif cadastro_opcao == "Filial":
        st.subheader("Cadastro de Filial")
        empresa = st.selectbox("Empresa", [e["Razão Social"] for e in st.session_state.empresas])
        cnpj = st.text_input("CNPJ")
        municipio = st.text_input("Município")
        uf = st.selectbox("UF", ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
        if st.button("Salvar"):
            st.session_state.filiais.append({"Empresa": empresa, "CNPJ": cnpj, "Município": municipio, "UF": uf})
            st.success("Filial cadastrada com sucesso!")

# API para consulta de CND Federal
def consultar_cnd_federal(cnpj):
    return {"status": "API em desenvolvimento", "CNPJ": cnpj}

# API para consulta de CND Estadual
def consultar_cnd_estadual(cnpj, uf):
    return {"status": "API em desenvolvimento", "CNPJ": cnpj, "UF": uf}

# API para emitir CRF Caixa
def emitir_crf_caixa(cnpj):
    return {"status": "API em desenvolvimento", "CNPJ": cnpj}

# Tarefas
if menu == "Tarefas":
    st.subheader("Gestão de Tarefas")
    filial = st.selectbox("Filial", [f["CNPJ"] for f in st.session_state.filiais])
    setor = st.selectbox("Setor", [s["Nome"] for s in st.session_state.setores])
    subcategoria = st.selectbox("Subcategoria", [sc["Nome"] for sc in st.session_state.subcategorias])
    nome_tarefa = st.text_input("Nome da Tarefa")
    competencia = st.date_input("Competência", datetime.today())
    vencimento = st.date_input("Vencimento")
    usuarios = st.multiselect("Usuários", [u["Nome"] for u in st.session_state.usuarios])
    
    if st.button("Criar Tarefa"):
        st.session_state.tarefas.append({"Filial": filial, "Setor": setor, "Subcategoria": subcategoria, "Nome": nome_tarefa, "Competência": competencia, "Vencimento": vencimento, "Usuários": usuarios})
        st.success("Tarefa criada com sucesso!")

# Relatórios
if menu == "Relatórios":
    st.subheader("Kanban de Tarefas")
    status_options = ["A Vencer", "Atraso", "Entregue no Prazo", "Entregue Fora do Prazo"]
    status = st.radio("Status", status_options)
    tarefas_filtradas = [t for t in st.session_state.tarefas if status in t.get("Status", "")]
    df = pd.DataFrame(tarefas_filtradas)
    st.write(df)
    
    st.subheader("Calendário de Tarefas")
    df_calendar = pd.DataFrame(st.session_state.tarefas)
    if not df_calendar.empty:
        st.write(df_calendar.sort_values(by="Vencimento"))
    else:
        st.write("Nenhuma tarefa cadastrada.")

if menu == "Configurações":
    st.subheader("Configurações do Sistema")
    if st.button("Limpar Dados"):
        st.session_state.clear()
        st.success("Dados resetados com sucesso!")
