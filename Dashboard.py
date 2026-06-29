import streamlit as st
import pandas as pd
import sqlite3
import bcrypt
import plotly.express as px

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Dashboard Educacional",
    page_icon="📊",
    layout="wide"
)

# =========================
# BANCO
# =========================

conn = sqlite3.connect("professores.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS professores(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha BLOB NOT NULL
)
""")

conn.commit()

# =========================
# SESSION
# =========================

if "logado" not in st.session_state:
    st.session_state.logado = False

if "nome" not in st.session_state:
    st.session_state.nome = ""

# =========================
# LOGIN / CADASTRO
# =========================

if not st.session_state.logado:

    st.title("🎓 Plataforma de Análise Educacional")

    aba1, aba2 = st.tabs(["🔑 Login", "📝 Cadastro"])

    # LOGIN
    with aba1:

        st.subheader("Entrar")

        email = st.text_input("Email")
        senha = st.text_input(
            "Senha",
            type="password"
        )

        if st.button("Entrar"):

            cursor.execute(
                "SELECT nome, senha FROM professores WHERE email=?",
                (email,)
            )

            usuario = cursor.fetchone()

            if usuario:

                nome_db = usuario[0]
                senha_db = usuario[1]

                if bcrypt.checkpw(
                    senha.encode(),
                    senha_db
                ):

                    st.session_state.logado = True
                    st.session_state.nome = nome_db

                    st.rerun()

            st.error("Email ou senha inválidos.")

    # CADASTRO
    with aba2:

        st.subheader("Cadastrar Professor")

        nome = st.text_input(
            "Nome Completo",
            key="cad_nome"
        )

        email = st.text_input(
            "Email",
            key="cad_email"
        )

        senha = st.text_input(
            "Senha",
            type="password",
            key="cad_senha"
        )

        if st.button("Cadastrar"):

            if not nome.strip():
                st.error("Informe o nome.")

            elif not email.strip():
                st.error("Informe o email.")

            elif "@" not in email:
                st.error("Email inválido.")

            elif len(senha) < 6:
                st.error(
                    "A senha deve possuir pelo menos 6 caracteres."
                )

            else:

                senha_hash = bcrypt.hashpw(
                    senha.encode(),
                    bcrypt.gensalt()
                )

                try:

                    cursor.execute(
                        """
                        INSERT INTO professores
                        (nome,email,senha)
                        VALUES (?,?,?)
                        """,
                        (nome, email, senha_hash)
                    )

                    conn.commit()

                    st.success(
                        "Professor cadastrado com sucesso!"
                    )

                except sqlite3.IntegrityError:
                    st.error(
                        "Este email já está cadastrado."
                    )

# =========================
# DASHBOARD
# =========================

else:

    st.sidebar.success(
        f"👨‍🏫 {st.session_state.nome}"
    )

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    st.title("📊 Dashboard Educacional")

    arquivo = st.file_uploader(
        "Envie um CSV",
        type=["csv"]
    )

    if arquivo:

        df = pd.read_csv(arquivo)

        # -------------------
        # FILTROS
        # -------------------

        st.sidebar.header("Filtros")

        for coluna in df.columns:

            if df[coluna].dtype == "object":

                valores = st.sidebar.multiselect(
                    coluna,
                    df[coluna].dropna().unique(),
                    default=df[coluna].dropna().unique()
                )

                if valores:
                    df = df[df[coluna].isin(valores)]

        # -------------------
        # KPIs
        # -------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Registros",
            len(df)
        )

        col2.metric(
            "Colunas",
            len(df.columns)
        )

        col3.metric(
            "Valores Vazios",
            int(df.isnull().sum().sum())
        )

        col4.metric(
            "Duplicados",
            int(df.duplicated().sum())
        )

        # -------------------
        # ABAS
        # -------------------

        aba1, aba2 = st.tabs([
            "📋 Dados",
            "📈 Análises"
        ])

        # -------------------
        # DADOS
        # -------------------

        with aba1:

            st.subheader("Base de Dados")

            st.dataframe(
                df,
                use_container_width=True
            )

        # -------------------
        # GRAFICOS
        # -------------------

        with aba2:

            st.subheader("Visualizações")

            colunas = df.columns.tolist()

            x = st.selectbox(
                "Eixo X",
                colunas
            )

            y = st.selectbox(
                "Eixo Y",
                colunas
            )

            graf1 = px.bar(
                df,
                x=x,
                y=y,
                title=f"{y} por {x}"
            )

            st.plotly_chart(
                graf1,
                use_container_width=True
            )

            if df[y].dtype != "object":

                graf2 = px.histogram(
                    df,
                    x=y,
                    title=f"Distribuição de {y}"
                )

                st.plotly_chart(
                    graf2,
                    use_container_width=True
                )

                graf3 = px.scatter(
                    df,
                    x=x,
                    y=y,
                    title=f"{x} x {y}"
                )

                st.plotly_chart(
                    graf3,
                    use_container_width=True
                )

            if df[x].dtype == "object":

                graf4 = px.pie(
                    df,
                    names=x,
                    title=f"Distribuição de {x}"
                )

                st.plotly_chart(
                    graf4,
                    use_container_width=True
                )

    else:

        st.info(
            "Faça upload de um CSV para visualizar os dados."
        )