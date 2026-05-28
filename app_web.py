import os

print("PASTA ATUAL:", os.getcwd())

from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "123"

# =========================
# BANCO DE DADOS
# =========================
def conectar():
    conn = sqlite3.connect("banco.db")
    return conn

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
    <h2>Login</h2>
    <form method="POST">
        <input name="usuario" placeholder="Usuário">
        <input name="senha" type="password" placeholder="Senha">
        <button type="submit">Entrar</button>
    </form>
    """

# =========================
# LOGOUT (opcional)
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

    # CADASTRAR
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]

        cursor.execute("""
        INSERT INTO clientes (nome, telefone)
        VALUES (?, ?)
        """, (nome, telefone))

        conn.commit()

    # LISTAR
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