import streamlit as st
import pandas as pd
import sqlite3
import hashlib

# Conectar ao banco de dados SQLite
conn = sqlite3.connect("tarefas.db", check_same_thread=False)
c = conn.cursor()

# Criar tabelas se não existirem
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, senha TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS empresas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cnpj TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, descricao TEXT, empresa_id INTEGER, usuario_id INTEGER, status TEXT DEFAULT 'Pendente', FOREIGN KEY(empresa_id) REFERENCES empresas(id), FOREIGN KEY(usuario_id) REFERENCES usuarios(id))''')
# Criar usuário admin padrão se não existir
senha_admin = hashlib.sha256("admin123".encode()).hexdigest()
c.execute("INSERT INTO usuarios (nome, senha) SELECT 'admin', ? WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE nome='admin')", (senha_admin,))
conn.commit()

# Função para hash de senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Configuração da interface do Streamlit
st.set_page_config(page_title="Gestão de Tarefas", layout="wide")
st.title("📋 Gestão de Tarefas")

# Autenticação de usuários
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if st.session_state.usuario_logado is None:
    st.subheader("🔐 Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        senha_hashed = hash_senha(senha)
        c.execute("SELECT * FROM usuarios WHERE nome=? AND senha=?", (usuario, senha_hashed))
        user = c.fetchone()
        if user:
            st.session_state.usuario_logado = usuario
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos!")
    st.stop()

menu = ["Empresas", "Usuários", "Tarefas", "Sair"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Empresas":
    st.subheader("🏢 Cadastro de Empresas")
    with st.form("empresa_form"):
        nome = st.text_input("Nome da Empresa")
        cnpj = st.text_input("CNPJ")
        submitted = st.form_submit_button("Salvar")
        if submitted:
            c.execute("INSERT INTO empresas (nome, cnpj) VALUES (?, ?)", (nome, cnpj))
            conn.commit()
            st.success("Empresa cadastrada com sucesso!")
    empresas_df = pd.read_sql("SELECT * FROM empresas", conn)
    st.dataframe(empresas_df)

elif choice == "Usuários":
    st.subheader("👤 Cadastro de Usuários")
    with st.form("usuario_form"):
        nome = st.text_input("Nome do Usuário")
        senha = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Salvar")
        if submitted:
            senha_hashed = hash_senha(senha)
            c.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, senha_hashed))
            conn.commit()
            st.success("Usuário cadastrado com sucesso!")
    usuarios_df = pd.read_sql("SELECT * FROM usuarios", conn)
    st.dataframe(usuarios_df)

elif choice == "Tarefas":
    st.subheader("📝 Gerenciamento de Tarefas")
    empresas = pd.read_sql("SELECT id, nome FROM empresas", conn)
    usuarios = pd.read_sql("SELECT id, nome FROM usuarios", conn)
    with st.form("tarefa_form"):
        nome = st.text_input("Nome da Tarefa")
        descricao = st.text_area("Descrição")
        empresa = st.selectbox("Empresa", empresas["nome"].tolist())
        usuario = st.selectbox("Usuário", usuarios["nome"].tolist())
        status = st.selectbox("Status", ["Pendente", "Em andamento", "Concluída"])
        submitted = st.form_submit_button("Salvar")
        if submitted:
            empresa_id = empresas.loc[empresas["nome"] == empresa, "id"].values[0]
            usuario_id = usuarios.loc[usuarios["nome"] == usuario, "id"].values[0]
            c.execute("INSERT INTO tarefas (nome, descricao, empresa_id, usuario_id, status) VALUES (?, ?, ?, ?, ?)", (nome, descricao, empresa_id, usuario_id, status))
            conn.commit()
            st.success("Tarefa cadastrada com sucesso!")
    tarefas_df = pd.read_sql("SELECT tarefas.id, tarefas.nome, tarefas.descricao, empresas.nome AS empresa, usuarios.nome AS usuario, tarefas.status FROM tarefas JOIN empresas ON tarefas.empresa_id = empresas.id JOIN usuarios ON tarefas.usuario_id = usuarios.id", conn)
    st.dataframe(tarefas_df)

elif choice == "Sair":
    st.session_state.usuario_logado = None
    st.experimental_rerun()

# Fechar conexão com o banco de dados
conn.close()
