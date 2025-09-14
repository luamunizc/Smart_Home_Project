from hub import *


casa = SmartHomeHub()

casa.comeca()

while True:

    print(f"\n=== SMART HOME HUB ===\n\
    1. Listar dispositivos\n\
    TODO 2. Mostrar dispositivo\n\
    3. Executar comando em dispositivo\n\
    TODO 4. Alterar atributo de dispositivo\n\
    TODO 5. Executar rotina\n\
    TODO 6. Gerar relatorio\n\
    7. Salvar configuracao\n\
    8. Adicionar dispositivo\n\
    9. Remover dispositivo\n\
    10. Sair\n\n")
    escolha = input(f"Escolha uma opcao:")
    escolha = escolha.strip()

    if escolha == "1":

        print()
        casa.print_list_all_devices()
        print()

    elif escolha == "2":

        print()
        em_uso = sel_disponiveis(casa.lista())
        print(em_uso)

    elif escolha == "3":

        print()
        em_uso = sel_disponiveis(casa.lista())
        casa.usar(em_uso)
        print(em_uso)


    elif escolha == "4":
        ...
    elif escolha == "5":
        ...
    elif escolha == "6":
        ...
    elif escolha == "7":

        casa.salvar_configuracao('data/casa.json')

    elif escolha == "8":

        tipo_selecionado = selecao_dispositivo()
        nome_selecionado = nome_dispositivo()
        casa.add_device(tipo_selecionado, nome_selecionado)

    elif escolha == "9":

        escolha = sel_disponiveis(casa.lista())
        casa.remove_device(escolha)

    elif escolha == "10":

        casa.salvar_configuracao('data/casa.json')
        print("Ate logo!")
        break

    else:
        print("Opcao invalida, tente novamente")

