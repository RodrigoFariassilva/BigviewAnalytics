import sqlite3
import bcrypt

def verificar_login(email, senha):

    conn = sqlite3.connect("professores.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT senha,nome FROM professores WHERE email=?",
        (email,)
    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:

        senha_hash = resultado[0]
        nome = resultado[1]

        if bcrypt.checkpw(
            senha.encode(),
            senha_hash
        ):
            return True, nome

    return False, None