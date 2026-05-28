import os
from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

# ISSO AQUI EXPLICA PARA O RENDER O CAMINHO EXATO DAS SUAS PASTAS
caminho_base = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(caminho_base, "templates"),
            static_folder=os.path.join(caminho_base, "static"))

app.secret_key = "123"

# =========================
# BANCO DE DADOS
# =========================
def conectar():
    # Garante que o banco.db será criado na pasta certa na nuvem
    banco_path = os.path.join(caminho_base, "banco.db")
    conn = sqlite3.connect(banco_path)
    return conn

# Cria a tabela automaticamente no lugar certo ao iniciar
conn = conectar()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    telefone TEXT
)
""")
conn.commit()
conn.close()

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == "admin" and senha == "123":
            session["logado"] = True
            return redirect(url_for("clientes"))

        return "Login inválido"

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
        <style>
            body {
                font-family: Arial;
                background: #f5f5f5;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            .box {
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
                width: 320px;
                text-align: center;
            }

            .titulo {
                background: #556B2F;
                color: white;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
            }

            .titulo h1 {
                font-size: 18px;
                margin: 0;
            }

            .titulo p {
                margin: 5px 0 0 0;
                color: #FFD700;
                font-size: 12px;
            }

            input {
                width: 90%;
                padding: 10px;
                margin: 8px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }

            button {
                width: 100%;
                padding: 10px;
                background: #556B2F;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }

            button:hover {
                background: #6B8E23;
            }
        </style>
    </head>

    <body>

    <div class="box">

        <div class="titulo">
            <h1>Espaço Josy Miranda Estética</h1>
            <p>Sistema de Gestão</p>
        </div>

        <form method="POST">
            <input name="usuario" placeholder="Usuário">
            <input name="senha" type="password" placeholder="Senha">
            <button type="submit">Entrar</button>
        </form>

    </div>

    </body>
    </html>
    """

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# =========================
# CLIENTES (CRUD)
# =========================
@app.route("/clientes", methods=["GET", "POST"])
def clientes():

    if not session.get("logado"):
        return redirect(url_for("login"))

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]

        cursor.execute("""
        INSERT INTO clientes (nome, telefone)
        VALUES (?, ?)
        """, (nome, telefone))

        conn.commit()

    cursor.execute("SELECT id, nome, telefone FROM clientes")
    lista = cursor.fetchall()

    conn.close()

    return render_template("clientes.html", clientes=lista)

# =========================
# EXCLUIR CLIENTE
# =========================
@app.route("/delete/<int:id>")
def delete(id):

    if not session.get("logado"):
        return redirect(url_for("login"))

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("clientes"))

# =========================
# INÍCIO
# =========================
@app.route("/")
def home():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)