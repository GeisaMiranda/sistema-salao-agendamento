import json

agendamentos = []

def salvar_agendamentos():
    with open("agendamentos.json", "w") as f:
        json.dump(agendamentos, f)


def carregar_agendamentos():
    global agendamentos
    try:
        with open("agendamentos.json", "r") as f:
            agendamentos = json.load(f)
    except FileNotFoundError:
        agendamentos = []

def agendar_horario():

    nome = input("Nome da cliente: ")

    servico = input("Serviço desejado: ")

    horario = input("Horário do atendimento: ")

    agendamento = {
        "nome": nome,
        "servico": servico,
        "horario": horario
    }

    agendamentos.append(agendamento)
    salvar_agendamentos()

    print("\nAgendamento realizado com sucesso!")

def listar_agendamentos():

    print("\n===== AGENDAMENTOS =====")

    for agenda in agendamentos:

        print("Cliente:", agenda["nome"])

        print("Serviço:", agenda["servico"])

        print("Horário:", agenda["horario"])

        print("--------------------")