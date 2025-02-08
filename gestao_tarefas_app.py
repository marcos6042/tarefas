import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import re
from hashlib import sha256
from typing import Dict, List

# Configuração do banco de dados
def init_db():
    conn = sqlite3.connect('tarefas.db')
    c = conn.cursor()
    
    # Criar tabelas necessárias
    c.execute('''CREATE TABLE IF NOT EXISTS empresas
                 (id INTEGER PRIMARY KEY, razao_social TEXT, cnpj TEXT UNIQUE)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS filiais
                 (id INTEGER PRIMARY KEY, empresa_id INTEGER, cnpj TEXT UNIQUE, 
                  tipo TEXT, municipio TEXT, uf TEXT, inscricao_estadual TEXT, 
                  senha_sefaz_hash TEXT)''')
    
    conn.commit()
    return conn

# Funções de validação
def validar_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    return len(cnpj) == 14

def validar_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Classe para gerenciar tarefas
class GerenciadorTarefas:
    def __init__(self, conn):
        self.conn = conn
    
    def adicionar_tarefa(self, dados: Dict) -> bool:
        try:
            c = self.conn.cursor()
            c.execute('''INSERT INTO tarefas 
                        (filial_id, setor_id, subcategoria_id, nome, competencia, 
                         vencimento, usuario_id, status) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                     (dados['filial_id'], dados['setor_id'], 
                      dados['subcategoria_id'], dados['nome'],
                      dados['competencia'], dados['vencimento'],
                      dados['usuario_id'], 'PENDENTE'))
            self.conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao adicionar tarefa: {str(e)}")
            return False
    
    def get_tarefas_kanban(self) -> Dict[str, List]:
        c = self.conn.cursor()
        c.execute('''SELECT t.*, f.nome as filial_nome, u.nome as usuario_nome
                     FROM tarefas t
                     JOIN filiais f ON t.filial_id = f.id
                     JOIN usuarios u ON t.usuario_id = u.id''')
        
        colunas = ['PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDO']
        tarefas = {col: [] for col in colunas}
        
        for row in c.fetchall():
            tarefas[row['status']].append({
                'id': row['id'],
                'nome': row['nome'],
                'filial': row['filial_nome'],
                'responsavel': row['usuario_nome'],
                'vencimento': row['vencimento']
            })
        
        return tarefas

# Interface principal
def main():
    st.set_page_config(page_title="Gestão de Tarefas - Grupo Rodoxisto", layout="wide")
    
    # Inicializar banco de dados
    conn = init_db()
    gerenciador = GerenciadorTarefas(conn)
    
    # Configuração de autenticação
    if 'user_id' not in st.session_state:
        mostrar_login()
        return
    
    # Menu principal
    st.sidebar.title("Menu")
    opcao = st.sidebar.selectbox(
        "Selecione uma opção",
        ["Cadastros", "Tarefas", "Relatórios"]
    )
    
    if opcao == "Cadastros":
        mostrar_cadastros()
    elif opcao == "Tarefas":
        mostrar_tarefas(gerenciador)
    else:
        mostrar_relatorios(gerenciador)

def mostrar_login():
    st.title("Login")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        if validar_credenciais(email, senha):
            st.session_state.user_id = get_user_id(email)
            st.experimental_rerun()
        else:
            st.error("Credenciais inválidas")

def mostrar_kanban(gerenciador):
    tarefas = gerenciador.get_tarefas_kanban()
    
    cols = st.columns(3)
    
    for i, status in enumerate(['PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDO']):
        with cols[i]:
            st.subheader(status.replace('_', ' '))
            for tarefa in tarefas[status]:
                with st.container():
                    st.markdown(f"""
                    **{tarefa['nome']}**  
                    Filial: {tarefa['filial']}  
                    Responsável: {tarefa['responsavel']}  
                    Vencimento: {tarefa['vencimento']}
                    """)
                    if status != 'CONCLUIDO':
                        if st.button(f"➡️ Mover", key=f"mover_{tarefa['id']}"):
                            mover_tarefa(gerenciador, tarefa['id'], status)

if __name__ == "__main__":
    main()
