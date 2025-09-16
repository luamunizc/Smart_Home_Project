# Projeto Smart Home - Avaliação Final de POO com Python

## Visão Geral

O presente projeto tem por objetivo implementar os conhecimentos de programação orientada a objetos estudados no curso, como herança, polimorfismo, abstração e encapsulamento. Além dos conceitos fundamentais de POO, o projeto explora o uso de módulos não built-in do Python, como o `transitions`, que auxilia na criação e no gerenciamento de máquinas de estado para os dispositivos da casa inteligente.

Este projeto simula um hub de automação residencial (Smart Home Hub) que permite ao usuário gerenciar diversos dispositivos inteligentes através de uma interface de linha de comando (CLI).

## Funcionalidades

A interface de linha de comando oferece as seguintes opções para interagir com o hub da casa inteligente:

* **1. Listar dispositivos:** Exibe uma lista com todos os dispositivos atualmente conectados ao hub.
* **2. Mostrar dispositivo:** Apresenta informações detalhadas sobre um dispositivo específico selecionado pelo usuário.
* **3. Executar comando em dispositivo:** Permite que o usuário execute ações específicas em um dispositivo (ex: ligar, desligar, alterar canal).
* **4. Alterar atributo de dispositivo:** Modifica um atributo de um dispositivo (ex: alterar a temperatura do ar condicionado).
* **5. Salvar configuração:** Salva o estado atual de todos os dispositivos em um arquivo `casa.json`.
* **6. Adicionar dispositivo:** Adiciona um novo dispositivo à casa, permitindo escolher o tipo e definir um nome.
* **7. Remover dispositivo:** Remove um dispositivo existente da configuração da casa.
* **8. Sair:** Encerra a aplicação, salvando automaticamente a configuração atual antes de fechar.

## Como Usar

1.  **Pré-requisitos:** Certifique-se de ter o Python versão 3.11 instalado, e com uma máquina virtual ativada, digite na linha de comando:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Estrutura de Arquivos:** O projeto se apresenta na estrutura de diretórios seguinte:
    ```
    /Smart_Home_Project
    |-- requirements.txt
    |-- central/
        |--__init__.py
        |-- cli.py
        |-- errors.py
        |-- hub.py
        |-- log.py
        |-- observers.py
        |-- devices/
            |--__init__.py
            |-- alarm.py
            |-- cam.py
            |-- devices.py
            |-- door.py
            |-- feeder.py
            |-- lamp.py
            |-- switch.py
    |-- data/
        |-- casa.json
        |-- log.csv
    
    ```

3.  **Execução:** Para iniciar o programa, execute o arquivo principal que contém o loop da CLI:
    ```bash
    python .\central\cli.py
    ```

4.  **Interação:** Após a execução, um menu interativo será exibido no terminal. Basta digitar o número da opção desejada e pressionar Enter para interagir com o sistema.


![Interface de Linha de Comando](data/CLI%20principal.png)

