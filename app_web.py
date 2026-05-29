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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_servico TEXT,
        preco REAL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        servico_id INTEGER,
        data TEXT,
        horario TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id),
        FOREIGN KEY(servico_id) REFERENCES servicos(id)
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
            background: url('/static/foto_josy.jpg');
            background-size: cover; 
            /* 'top' faz a foto começar de cima para baixo */
            background-position: top center; 
            background-attachment: fixed;
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh;
            margin: 0;
        }

        /* Camada que escurece/clareia a foto de fundo */
        body::before {
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255, 255, 255, 0.4); /* Ajuste este valor: 0.4 deixa a foto mais visível, 0.8 deixa mais branca */
            z-index: -1; /* Coloca a camada atrás de tudo */
        }

        .box { 
            background: white; /* Caixa branca sólida */
            padding: 25px; 
            border-radius: 10px; 
            box-shadow: 0px 4px 15px rgba(0,0,0,0.3); 
            width: 320px; 
            text-align: center;
            opacity: 1; /* Garante que a caixa não fique transparente */
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
    
    # Se a dona do salão enviar o formulário de cadastrar cliente
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        cursor.execute("""
            INSERT INTO clientes (nome, telefone) 
            VALUES (?, ?)
        """, (nome, telefone))
        conn.commit()
    
    # 1. Puxa todos os clientes para listar na tela
    cursor.execute("SELECT id, nome, telefone FROM clientes")
    lista_clientes = cursor.fetchall()
    
    # 2. Puxa todos os serviços para listar na tela
    cursor.execute("SELECT id, nome_servico, preco FROM servicos")
    lista_servicos = cursor.fetchall()
    
    # 3. Puxa os agendamentos juntando os nomes de quem vai fazer o quê (INNER JOIN)
    cursor.execute("""
        SELECT agendamentos.id, clientes.nome, servicos.nome_servico, agendamentos.data, agendamentos.horario 
        FROM agendamentos
        INNER JOIN clientes ON agendamentos.cliente_id = clientes.id
        INNER JOIN servicos ON agendamentos.servico_id = servicos.id
    """)
    lista_agendamentos = cursor.fetchall()
    
    conn.close()
    
    # Envia as 3 listas organizadas para o HTML
    return render_template("clientes.html", 
                           clientes=lista_clientes, 
                           servicos=lista_servicos, 
                           agendamentos=lista_agendamentos)

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
# ROTAS DE SERVIÇOS E AGENDAMENTOS
# =========================

@app.route("/salvar_servico", methods=["POST"])
def salvar_servico():
    nome = request.form["nome_servico"]
    preco = request.form["preco"]
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO servicos (nome_servico, preco) VALUES (?, ?)", (nome, preco))
    conn.commit()
    conn.close()
    return redirect(url_for("clientes"))

@app.route("/deletar_servico/<int:id>")
def deletar_servico(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM servicos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("clientes"))

@app.route("/salvar_agendamento", methods=["POST"])
def salvar_agendamento():
    cliente_id = request.form["cliente_id"]
    servico_id = request.form["servico_id"]
    data = request.form["data"]
    horario = request.form["horario"]
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO agendamentos (cliente_id, servico_id, data, horario) VALUES (?, ?, ?, ?)", 
                   (cliente_id, servico_id, data, horario))
    conn.commit()
    conn.close()
    return redirect(url_for("clientes"))

@app.route("/deletar_agendamento/<int:id>")
def deletar_agendamento(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agendamentos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("clientes"))

# =========================
# INÍCIO
# =========================
@app.route("/")
def home():
    return "TESTE DE ATUALIZAÇÃO 123 - SE VOCÊ VÊ ISSO, O SITE ATUALIZOU!"

if __name__ == "__main__":
    app.run(debug=True)