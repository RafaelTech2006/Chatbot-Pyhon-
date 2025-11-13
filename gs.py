# INTEGRANTES:
# - Rafael Tavares Santos | RM: 563487
# - Gabriel Oliveira Amaral | RM: 563872
# - Felipe Yamagushi Mesquita | RM: 556170

# PROJETO: AGENDAMETO / CONSULTA MÉDICA

from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_core.documents import Document 
from langchain_community.vectorstores import Chroma 

menu = {
    'Horário' : [
        '8:00',
        '9:00',
        '10:00',
        '11:00',
        '13:00',
        '14:00',
        '15:00',
        '16:00'],

   'Dia' : [
       '11/11/2025',
        '12/11/2025',
        '13/11/2025',
        '14/11/2025',
        '15/11/2025'],

    'Exame' : [
        'Hemograma Completo',
        'Glicemia',
        'Colesterol Total',
        'Triglicerídeos',
        'Urina Tipo I'],
        
    'Medico' : [
        'Dr. João Silva',
        'Dra. Maria Oliveira',
        'Dr. Carlos Souza',
        'Dra. Ana Pereira',
        'Dr. Pedro Costa'],

    'Agendamentos': []
        
}


def forca_opcao(msg, conjunto_opcoes):
    opcoes = '\n'.join(conjunto_opcoes)
    escolha = input(f"{msg}\n{opcoes}\n-> ")
    while escolha not in conjunto_opcoes:
        print("Inválido.")
        escolha = input(f"{msg}\n{opcoes}\n-> ")
    return escolha

def exames_marcados():
    if not menu['Agendamentos']:
        print("\nVocê não possui exames agendados.\n")
        return
    print("\nExames agendados:")
    for i, ag in enumerate(menu['Agendamentos']):
        print(f"{i + 1}. Dia: {ag['Dia']} | Horário: {ag['Horário']} | Exame: {ag['Exame']} | Médico: {ag['Medico']}")
    print()

def agendamento():
    novo = {}
    for key in ['Dia', 'Horário', 'Exame', 'Medico']:
        info = forca_opcao(f"Escolha o {key} desejado:", menu[key])
        novo[key] = info

    menu['Agendamentos'].append(novo)
    print("\nAgendamento realizado com sucesso!\n")

def desmarcar_agendamento():
    if not menu['Agendamentos']:
        print("\nVocê não possui exames agendados para desmarcar.\n")
        return
    
    exames_marcados()
    try:
        indice = int(input("Digite o número do agendamento que deseja desmarcar: ")) - 1
        if 0 <= indice < len(menu['Agendamentos']):
            menu['Agendamentos'].pop(indice)
            print("\nAgendamento desmarcado com sucesso!\n")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

def atualizar_agendamento():
    if not menu['Agendamentos']:
        print("\nVocê não possui exames agendados para atualizar.\n")
        return
    
    exames_marcados()
    try:
        indice = int(input("Digite o número do agendamento que deseja atualizar: ")) - 1
        if 0 <= indice < len(menu['Agendamentos']):
            agendamento = menu['Agendamentos'][indice]
            for key in ['Dia', 'Horário', 'Exame', 'Medico']:
                alteracao = input(f"Novo {key} (pressione Enter para manter o atual: {agendamento[key]}): ")
                if alteracao:
                    agendamento[key] = alteracao
            print("\nAgendamento atualizado com sucesso!\n")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

# === Dicionário de ações ===
opcoes = {
    'agendar': agendamento,
    'agendamento': agendamento,
    'marcar': agendamento,
    'ver': exames_marcados,
    'consultar': exames_marcados,
    'atualizar': atualizar_agendamento,
    'editar': atualizar_agendamento,
    'cancelar': desmarcar_agendamento,
    'desmarcar': desmarcar_agendamento
}

# === Base de conhecimento do CRUD ===
documentos_crud = [
    Document(
        page_content="Para agendar um exame, selecione a opção de agendamento. Você deverá escolher o Dia, Horário, Exame e Médico desejado.",
        metadata={"categoria": "agendamento"}
    ),
    Document(
        page_content="Para visualizar os seus exames marcados, escolha a opção de consulta. Serão mostrados todos os seus exames com Dia, Horário, Exame e Médico.",
        metadata={"categoria": "consulta"}
    ),
    Document(
        page_content="Para atualizar um agendamento, escolha a opção de atualização. Digite o número do agendamento e insira os novos dados.",
        metadata={"categoria": "atualizacao"}
    ),
    Document(
        page_content="Para desmarcar um exame, escolha a opção de desmarcação. Digite o número do agendamento que deseja desmarcar.",
        metadata={"categoria": "desmarcamento"}
    ),
    Document(
        page_content="Para sair do sistema, digite 'sair'.",
        metadata={"categoria": "saida"}
    )
]

# === Modelo de embeddings ===
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# === Banco vetorial (Chroma) ===
chroma_db = Chroma.from_documents(documentos_crud, embedding=embeddings)

# === Chatbot ===
print("Olá! Eu sou o ChatMed — seu assistente virtual para agendamento de exames.\nDigite 'sair' para encerrar.\n")

while True:
    pergunta = input("Você: ").lower().strip()
    if pergunta in ["sair", "exit", "quit"]:
        print("ChatMed: Obrigado por usar o ChatMed! Até a próxima.")
        break

    # Tenta detectar intenção antes da busca
    acao_executada = False
    for palavra, funcao in opcoes.items():
        if palavra in pergunta:
            funcao()
            acao_executada = True
            break

    if not acao_executada:
        resultados = chroma_db.similarity_search(pergunta, k=1)
        if resultados:
            resposta = resultados[0].page_content
            print(f"ChatMed: {resposta}\n")
        else:
            print("ChatMed: Desculpe, não foi possível encontrar nenhuma resposta.\n")