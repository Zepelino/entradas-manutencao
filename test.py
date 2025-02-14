import os
from datetime import datetime
from PySimpleGUI import PySimpleGUI as sg
import uuid  # Para gerar IDs únicos

# Caminho do arquivo .txt que substituirá o banco de dados
DATA_FILE = "entradas.txt"

# Função para carregar os dados do arquivo .txt
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return [line.strip().split("#$%") for line in file.readlines()]

# Função para salvar os dados no arquivo .txt
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        for entry in data:
            file.write("#$%".join(entry) + "\n")

# Função para adicionar uma nova entrada
def add_entry(cliente, tipo, fabricante, id_equipamento, orcamento, data_entrada, data_saida=""):
    id_unico = str(uuid.uuid4())  # Gera um ID único
    nova_entrada = [id_unico, cliente, tipo, fabricante, id_equipamento, orcamento, data_entrada, data_saida]
    data = load_data()
    data.append(nova_entrada)
    save_data(data)

# Função para buscar entradas com base em critérios
def search_entries(cliente="", tipo="", fabricante="", id_equipamento="", data_entrada=""):
    data = load_data()
    resultados = []
    for entry in data:
        if (cliente.lower() in entry[1].lower() and
            tipo.lower() in entry[2].lower() and
            fabricante.lower() in entry[3].lower() and
            id_equipamento.lower() in entry[4].lower() and
            data_entrada in entry[6]):
            resultados.append(entry)
    # Ordena os resultados pela data de entrada (do mais recente para o mais antigo)
    resultados.sort(key=lambda x: datetime.strptime(x[6], "%d/%m/%Y"), reverse=True)
    return resultados

# Função para atualizar uma entrada existente
def update_entry(id_unico, new_entry):
    data = load_data()
    for i, entry in enumerate(data):
        if entry[0] == id_unico:  # Compara o ID único
            data[i] = new_entry
            break
    save_data(data)

# Função para deletar uma entrada
def delete_entry(id_unico):
    data = load_data()
    data = [entry for entry in data if entry[0] != id_unico]  # Remove a entrada com o ID único
    save_data(data)

# Função principal para criar a interface gráfica
def create_main_window():
    sg.theme("Reddit")

    # Layout da tela principal
    layout_main = [
        [sg.Text('Arrumador 3000', font='Helvetica 32 bold', expand_x=True, justification='center', pad=(0, 20))],
        [sg.Button('Buscar no registo', font='Helvetica 16', key="-btRead-", size=(20, 2), pad=(10, 10)),
         sg.Button('Adicionar ao registro', font='Helvetica 16', key="-btWrite-", size=(20, 2), pad=(10, 10))]
    ]

    # Layout da tela de escrita
    layout_write = [
        [sg.Text('Gravador 3000', font='Helvetica 32 bold', expand_x=True, justification='center', pad=(0, 20))],
        [sg.Text('Cliente:', size=(15, 1)), sg.Input(key='-inpWClient-', size=(40, 1))],
        [sg.Text('Tipo do equipamento:', size=(15, 1)), sg.Input(key='-inpWType-', size=(40, 1))],
        [sg.Text('Fabricante:', size=(15, 1)), sg.Input(key='-inpWFab-', size=(40, 1))],
        [sg.Text('Identificação:', size=(15, 1)), sg.Input(key='-inpWID-', size=(40, 1))],
        [sg.Text('Orçamento:', size=(15, 1)), sg.Multiline(key='-inpWBudget-', size=(40, 5))],
        [sg.Text('Data de entrada:', size=(15, 1)), sg.Input(key='-inpWArrive-', size=(40, 1))],
        [sg.Button('Cancelar', key='-btWCancel-', size=(10, 1), pad=(10, 20)),
         sg.Button('Submeter', key='-btWSub-', size=(10, 1), pad=(10, 20))]
    ]

    # Layout da tela de busca
    layout_search = [
        [sg.Text('Procuração 3000', font='Helvetica 32 bold', expand_x=True, justification='center', pad=(0, 20))],
        [sg.Text('Cliente:', size=(15, 1)), sg.Input(key='-inpSClient-', size=(40, 1))],
        [sg.Text('Tipo do equipamento:', size=(15, 1)), sg.Input(key='-inpSType-', size=(40, 1))],
        [sg.Text('Fabricante:', size=(15, 1)), sg.Input(key='-inpSFab-', size=(40, 1))],
        [sg.Text('Identificação:', size=(15, 1)), sg.Input(key='-inpSID-', size=(40, 1))],
        [sg.Text('Data de entrada:', size=(15, 1)), sg.Input(key='-inpSArrive-', size=(40, 1))],
        [sg.Button('Cancelar', key='-btSCancel-', size=(10, 1), pad=(10, 20)),
         sg.Button('Procurar', key='-btSSub-', size=(10, 1), pad=(10, 20))]
    ]

    # Layout da lista de resultados
    layout_search_list = [
        [sg.Text('Lista de Resultados', font='Helvetica 32 bold', expand_x=True, justification='center', pad=(0, 20))],
        [sg.Table(values=[], headings=['Cliente', 'Equipamento', 'Fabricante', 'ID Equipamento', 'Data Entrada', 'Data Saída'],
                  auto_size_columns=True, justification='left', num_rows=10, key='-results_table-', pad=(10, 10))],
        [sg.Button('Voltar', key='-btSLBack-', size=(10, 1), pad=(10, 20)),
         sg.Button('Acessar', key='-btSLAccess-', size=(10, 1), pad=(10, 20))]
    ]

    # Layout da tela de leitura
    layout_read = [
        [sg.Text('Leitura 3000', font='Helvetica 32 bold', expand_x=True, justification='center', pad=(0, 20))],
        [sg.Text('Cliente:', size=(15, 1)), sg.Text('', key='rd_client', size=(40, 1))],
        [sg.Text('Equipamento:', size=(15, 1)), sg.Text('', key='rd_equip', size=(40, 1))],
        [sg.Text('Fabricante:', size=(15, 1)), sg.Text('', key='rd_fab', size=(40, 1))],
        [sg.Text('Identificação:', size=(15, 1)), sg.Text('', key='rd_id', size=(40, 1))],
        [sg.Text('Data de entrada:', size=(15, 1)), sg.Text('', key='rd_arrive_date', size=(40, 1))],
        [sg.Text('Data de saída:', size=(15, 1)), sg.Text('', key='rd_depart_date', size=(40, 1))],
        [sg.Text('Orçamento:', size=(15, 1)), sg.Multiline('', key='rd_budget', size=(40, 5), disabled=True)],
        [sg.Button('Voltar', key='-btRBack-', size=(10, 1), pad=(10, 20)),
         sg.Button('Editar', key='-btREdit-', size=(10, 1), pad=(10, 20))]
    ]

    # Layout da tela de edição
    layout_edit = [
        [sg.Text('Editor 3000', font='Helvetica 32 bold', expand_x=True, justification='center', pad=(0, 20))],
        [sg.Text('Cliente:', size=(15, 1)), sg.Input(key='-inpEClient-', size=(40, 1))],
        [sg.Text('Tipo do equipamento:', size=(15, 1)), sg.Input(key='-inpEType-', size=(40, 1))],
        [sg.Text('Fabricante:', size=(15, 1)), sg.Input(key='-inpEFab-', size=(40, 1))],
        [sg.Text('Identificação:', size=(15, 1)), sg.Input(key='-inpEID-', size=(40, 1))],
        [sg.Text('Orçamento:', size=(15, 1)), sg.Multiline(key='-inpEBudget-', size=(40, 5))],
        [sg.Text('Data de chegada:', size=(15, 1)), sg.Input(key='-EArriveDate-', size=(40, 1))],
        [sg.Text('Data de saída:', size=(15, 1)), sg.Input(key='-EDepartureDate-', size=(40, 1))],
        [sg.Button('Cancelar', key='-btECancel-', size=(10, 1), pad=(10, 20)),
         sg.Button('Modificar', key='-btESub-', size=(10, 1), pad=(10, 20)),
         sg.Button('Deletar', key='-btEDelete-', size=(10, 1), button_color=('white', 'red'), pad=(10, 20))]
    ]

    # Layout geral
    layout = [
        [sg.Column(layout_main, key='-MAIN_PAGE-', visible=True),
         sg.Column(layout_write, key='-WRITE_PAGE-', visible=False),
         sg.Column(layout_search, key='-SEARCH_PAGE-', visible=False),
         sg.Column(layout_search_list, key='-SEARCH_LIST_PAGE-', visible=False),
         sg.Column(layout_read, key='-READ_PAGE-', visible=False),
         sg.Column(layout_edit, key='-EDIT_PAGE-', visible=False)]
    ]

    window = sg.Window("Arrumador 3000", layout, finalize=True)

    state = "MAIN"
    resultados = []  # Armazena os resultados da busca

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if state == "MAIN":
            if event == "-btRead-":
                # Limpa os campos de busca ao mudar para a aba de busca
                window['-inpSClient-'].update('')
                window['-inpSType-'].update('')
                window['-inpSFab-'].update('')
                window['-inpSID-'].update('')
                window['-inpSArrive-'].update('')
                window['-MAIN_PAGE-'].update(visible=False)
                window['-SEARCH_PAGE-'].update(visible=True)
                state = "SEARCH"

            if event == "-btWrite-":
                # Limpa os campos de escrita ao mudar para a aba de escrita
                window['-inpWClient-'].update('')
                window['-inpWType-'].update('')
                window['-inpWFab-'].update('')
                window['-inpWID-'].update('')
                window['-inpWBudget-'].update('')
                window['-inpWArrive-'].update('')
                window['-MAIN_PAGE-'].update(visible=False)
                window['-WRITE_PAGE-'].update(visible=True)
                state = "WRITE"

        elif state == "WRITE":
            if event == "-btWCancel-":
                window['-WRITE_PAGE-'].update(visible=False)
                window['-MAIN_PAGE-'].update(visible=True)
                state = "MAIN"

            if event == "-btWSub-":
                cliente = values['-inpWClient-']
                tipo = values['-inpWType-']
                fabricante = values['-inpWFab-']
                id_equipamento = values['-inpWID-']
                orcamento = values['-inpWBudget-']
                data_entrada = values['-inpWArrive-']

                # Se a data de entrada estiver vazia, usa a data de hoje
                if not data_entrada.strip():
                    data_entrada = datetime.now().strftime("%d/%m/%Y")
                else:
                    # Verifica se a data está no formato correto
                    try:
                        datetime.strptime(data_entrada, "%d/%m/%Y")
                    except ValueError:
                        sg.popup("Formato de data inválido! Use o formato dd/mm/aaaa.")
                        continue

                add_entry(cliente, tipo, fabricante, id_equipamento, orcamento, data_entrada)
                sg.popup("Entrada adicionada com sucesso!")
                window['-WRITE_PAGE-'].update(visible=False)
                window['-MAIN_PAGE-'].update(visible=True)
                state = "MAIN"

        elif state == "SEARCH":
            if event == "-btSCancel-":
                window['-SEARCH_PAGE-'].update(visible=False)
                window['-MAIN_PAGE-'].update(visible=True)
                state = "MAIN"

            if event == "-btSSub-":
                cliente = values['-inpSClient-']
                tipo = values['-inpSType-']
                fabricante = values['-inpSFab-']
                id_equipamento = values['-inpSID-']
                data_entrada = values['-inpSArrive-']

                resultados = search_entries(cliente, tipo, fabricante, id_equipamento, data_entrada)
                if resultados:
                    # Formata os resultados para exibição na tabela (sem o ID único)
                    resultados_formatados = []
                    for entry in resultados:
                        data_entrada_formatada = entry[6]  # Já está no formato dd/mm/aaaa
                        data_saida_formatada = entry[7] if entry[7] else "Ainda na empresa"
                        resultados_formatados.append([
                            entry[1],  # Cliente
                            entry[2],  # Equipamento
                            entry[3],  # Fabricante
                            entry[4],  # ID Equipamento
                            data_entrada_formatada,  # Data de entrada
                            data_saida_formatada  # Data de saída
                        ])

                    window['-results_table-'].update(values=resultados_formatados)
                    window['-SEARCH_PAGE-'].update(visible=False)
                    window['-SEARCH_LIST_PAGE-'].update(visible=True)
                    state = "SEARCH_LIST"
                else:
                    sg.popup("Nenhum resultado encontrado.")

        elif state == "SEARCH_LIST":
            if event == "-btSLBack-":
                window['-SEARCH_LIST_PAGE-'].update(visible=False)
                window['-SEARCH_PAGE-'].update(visible=True)
                state = "SEARCH"

            if event == "-btSLAccess-":
                if not values['-results_table-']:
                    sg.popup("Selecione uma entrada para acessar.")
                    continue

                selected_entry_index = values['-results_table-'][0]
                selected_entry = resultados[selected_entry_index]  # Usa o ID único internamente

                # Preenche a tela de leitura com os dados selecionados
                window['rd_client'].update(selected_entry[1])
                window['rd_equip'].update(selected_entry[2])
                window['rd_fab'].update(selected_entry[3])
                window['rd_id'].update(selected_entry[4])
                window['rd_arrive_date'].update(selected_entry[6])  # Já está no formato dd/mm/aaaa
                window['rd_depart_date'].update(selected_entry[7] if selected_entry[7] else "Ainda na empresa")
                window['rd_budget'].update(selected_entry[5])

                window['-SEARCH_LIST_PAGE-'].update(visible=False)
                window['-READ_PAGE-'].update(visible=True)
                state = "READ"

        elif state == "READ":
            if event == "-btRBack-":
                window['-READ_PAGE-'].update(visible=False)
                window['-SEARCH_LIST_PAGE-'].update(visible=True)
                state = "SEARCH_LIST"

            if event == "-btREdit-":
                # Preenche a tela de edição com os dados atuais
                window['-inpEClient-'].update(window['rd_client'].get())
                window['-inpEType-'].update(window['rd_equip'].get())
                window['-inpEFab-'].update(window['rd_fab'].get())
                window['-inpEID-'].update(window['rd_id'].get())
                window['-inpEBudget-'].update(window['rd_budget'].get())
                window['-EArriveDate-'].update(window['rd_arrive_date'].get())
                window['-EDepartureDate-'].update(window['rd_depart_date'].get())

                window['-READ_PAGE-'].update(visible=False)
                window['-EDIT_PAGE-'].update(visible=True)
                state = "EDIT"

        elif state == "EDIT":
            if event == "-btECancel-":
                window['-EDIT_PAGE-'].update(visible=False)
                window['-READ_PAGE-'].update(visible=True)
                state = "READ"

            if event == "-btESub-":
                cliente = values['-inpEClient-']
                tipo = values['-inpEType-']
                fabricante = values['-inpEFab-']
                id_equipamento = values['-inpEID-']
                orcamento = values['-inpEBudget-']
                data_entrada = values['-EArriveDate-']
                data_saida = values['-EDepartureDate-']

                # Verifica se a data de entrada está no formato correto
                try:
                    datetime.strptime(data_entrada, "%d/%m/%Y")
                except ValueError:
                    sg.popup("Formato de data inválido! Use o formato dd/mm/aaaa.")
                    continue

                # Obtém o ID único da entrada selecionada
                selected_entry_index = values['-results_table-'][0]
                id_unico = resultados[selected_entry_index][0]

                # Cria a nova entrada com o mesmo ID único
                new_entry = [
                    id_unico,  # Mantém o mesmo ID único
                    cliente, tipo, fabricante, id_equipamento, orcamento, data_entrada, data_saida
                ]

                # Atualiza a entrada no arquivo .txt
                update_entry(id_unico, new_entry)

                # Atualiza a tela de leitura com os novos dados
                window['rd_client'].update(cliente)
                window['rd_equip'].update(tipo)
                window['rd_fab'].update(fabricante)
                window['rd_id'].update(id_equipamento)
                window['rd_arrive_date'].update(data_entrada)
                window['rd_depart_date'].update(data_saida if data_saida else "Ainda na empresa")
                window['rd_budget'].update(orcamento)

                sg.popup("Entrada atualizada com sucesso!")
                window['-EDIT_PAGE-'].update(visible=False)
                window['-READ_PAGE-'].update(visible=True)
                state = "READ"

            if event == "-btEDelete-":
                # Confirmação antes de deletar
                confirm = sg.popup_yes_no("Tem certeza que deseja deletar esta entrada?", title="Confirmar Deleção")
                if confirm == "Yes":
                    # Obtém o ID único da entrada selecionada
                    selected_entry_index = values['-results_table-'][0]
                    id_unico = resultados[selected_entry_index][0]

                    # Deleta a entrada
                    delete_entry(id_unico)

                    sg.popup("Entrada deletada com sucesso!")
                    window['-EDIT_PAGE-'].update(visible=False)
                    window['-MAIN_PAGE-'].update(visible=True)
                    state = "MAIN"

    window.close()

# Iniciar a interface gráfica
create_main_window()