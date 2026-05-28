import json

clientes = []

def salvar_clientes():
    with open("clientes.json", "w") as f:
        json.dump(clientes, f)


def carregar_clientes():
    global clientes
    try:
        with open("clientes.json", "r") as f:
            clientes = json.load(f)
    except FileNotFoundError:
        clientes = []

def cadastrar_cliente():

    nome = input("Digite o nome da cliente: ")

    telefone = input("Digite o telefone: ")

    cliente = {
        "nome": nome,
        "telefone": telefone
    }

    clientes.append(cliente)
    salvar_clientes()  

    print("\nCliente cadastrada com sucesso!")

def listar_clientes():

    print("\n===== CLIENTES CADASTRADOS =====")

    for cliente in clientes:

        print("Nome:", cliente["nome"])

        print("Telefone:", cliente["telefone"])

        print("-------------------")