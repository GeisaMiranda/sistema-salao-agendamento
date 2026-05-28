import sqlite3

def restaurar():
    # Conecta ao arquivo do seu banco
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()

    print("Verificando e criando tabelas...")
    
    # 1. Garante que a tabela de usuários existe (ajuste os nomes se o seu projeto usar outros)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
    """)
    
    # 2. Insere um usuário padrão (mude aqui para o login que você quer usar)
    login_teste = "admin"
    senha_teste = "admin123" # Se o seu código usar criptografia, precisaremos ajustar este ponto
    
    try:
        cursor.execute("""
            INSERT INTO usuarios (usuario, senha) 
            VALUES (?, ?)
        """, (login_teste, senha_teste))
        conn.commit()
        print(f"Sucesso! Usuário '{login_teste}' com a senha '{senha_teste}' foi cadastrado.")
    except sqlite3.IntegrityError:
        print(f"O usuário '{login_teste}' já existe no banco de dados.")
    except Exception as e:
        print("Erro ao inserir:", e)
        
    conn.close()

if __name__ == "__main__":
    restaurar()