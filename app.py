from clientes import cadastrar_cliente, listar_clientes, carregar_clientes
from agendamento import agendar_horario, listar_agendamentos, carregar_agendamentos
from servicos import listar_servicos

carregar_clientes()
carregar_agendamentos()

while True:

    print("\n===== SERVIÇO DO ESPAÇO JOSY MIRANDA ESTÉTICA =====")

    print("1 - Cadastrar Cliente")
    print("2 - Listar Clientes")
    print("3 - Agendar Horário")
    print("4 - Listar Agendamentos")
    print("5 - Servicos")
    print("6 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_cliente()

    elif opcao == "2":
        listar_clientes()

    elif opcao == "3":
        agendar_horario()

    elif opcao == "4":
        listar_agendamentos()

    elif opcao == "5":
        listar_servicos()

    elif opcao == "6":
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida")