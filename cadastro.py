import streamlit as st
import sqlite3
import bcrypt

st.title("Cadastro de Professor")

nome = st.text_input("Nome")
email = st.text_input("Email")
senha = st.text_input("Senha", type="password")

if st.button("Cadastrar"):

    senha_hash = bcrypt.hashpw(
        senha.encode(),
        bcrypt.gensalt()
    )

    try:
        conn = sqlite3.connect("professores.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO professores (nome,email,senha) VALUES (?,?,?)",
            (nome, email, senha_hash)
        )

        conn.commit()
        conn.close()

        st.success("Professor cadastrado!")

    except:
        st.error("Email já cadastrado.")