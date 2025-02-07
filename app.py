import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Gestão de Tarefas - Grupo Rodoxisto", layout="wide")

# Exibir logo
st.image("logo.jpeg", width=300)

st.title("Gestão de Tarefas - Grupo Rodoxisto")

# Tela Principal
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

# Controle de Navegação
if "page" in st.session_state:
    if st.session_state.page == "Nova Tarefa":
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
    
    elif st.session_state.page == "Kanban":
        st.subheader("Kanban de Tarefas")
        status_options = ["A Vencer", "Atraso", "Entregue no Prazo", "Entregue Fora do Prazo"]
        status = st.radio("Status", status_options)
        tarefas_filtradas = [t for t in st.session_state.tarefas if status in t.get("Status", "")]
        df = pd.DataFrame(tarefas_filtradas)
        st.write(df)
        
    elif st.session_state.page == "Calendário":
        st.subheader("Calendário de Tarefas")
        df_calendar = pd.DataFrame(st.session_state.tarefas)
        if not df_calendar.empty:
            st.write(df_calendar.sort_values(by="Vencimento"))
        else:
            st.write("Nenhuma tarefa cadastrada.")
    
    elif st.session_state.page == "Lista":
        st.subheader("Lista de Tarefas")
        df_list = pd.DataFrame(st.session_state.tarefas)
        st.write(df_list)

if st.button("Voltar para o Menu Principal"):
    st.session_state.page = ""
