from hub import *


casa = SmartHomeHub()

casa.comeca()

while True:

    print(f"\n=== SMART HOME HUB ===\n\n"
    f"1. Listar dispositivos\n"
    f"2. Mostrar dispositivo\n"
    f"3. Executar comando em dispositivo\n"
    f"4. Alterar atributo de dispositivo\n"
    # f"TODO 5. Executar rotina\n"
    # f"TODO 6. Gerar relatorio\n"
    f"7. Salvar configuracao\n"
    f"8. Adicionar dispositivo\n"
    f"9. Remover dispositivo\n"
    f"10. Sair\n")
    escolha = input(f"Escolha uma opcao:")
    escolha = escolha.strip()

    if escolha == "1":

        print()
        casa.print_list_all_devices()
        print()

    elif escolha == "2":

        print()
        em_uso = sel_disponiveis(casa.lista())
        print(casa.devices[em_uso].__str__())

    elif escolha == "3":

        print()
        em_uso = sel_disponiveis(casa.lista())
        casa.usar(em_uso)


    elif escolha == "4":

        em_uso = sel_disponiveis(casa.lista())
        casa.atributos(em_uso)

    elif escolha == "5":
        ...
    elif escolha == "6":
        ...
    elif escolha == "7":

        casa.salvar_configuracao('data/casa.json')

    elif escolha == "8":

        tipo_selecionado = selecao_dispositivo()
        nome_selecionado = nome_dispositivo()
        adicionar = {'type': tipo_selecionado, 'name': nome_selecionado}
        casa.add_device(adicionar, nome_selecionado)

    elif escolha == "9":

        escolha = sel_disponiveis(casa.lista())
        casa.remove_device(escolha)

    elif escolha == "10":

        casa.salvar_configuracao('data/casa.json')
        print("Ate logo!")
        break

    else:
        print("Opcao invalida, tente novamente")

