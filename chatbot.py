from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

# === Base de conhecimento do CRUD ===
documentos_crud = [
    Document(
        page_content=(
            "Para agendar um exame, selecione a opção 1 do menu. "
            "Você deverá escolher o Dia, Horário, Exame e Médico desejado."
        ),
        metadata={"categoria": "agendamento"}
    ),
    Document(
        page_content=(
            "Para visualizar os seus exames marcados, selecione a opção 2 do menu. "
            "Serão mostrados todos os seus exames com Dia, Horário, Exame e Médico."
        ),
        metadata={"categoria": "consulta"}
    ),
    Document(
        page_content=(
            "Para atualizar um agendamento, escolha a opção 3 do menu. "
            "Digite o número do agendamento e insira os novos dados."
        ),
        metadata={"categoria": "atualizacao"}
    ),
    Document(
        page_content=(
            "Para desmarcar um exame, escolha a opção 4 do menu. "
            "Digite o número do agendamento que deseja desmarcar."
        ),
        metadata={"categoria": "desmarcamento"}
    ),
    Document(
        page_content="Para sair do sistema, escolha a opção 5 do menu.",
        metadata={"categoria": "saída"}
    )
]

# === Criação do modelo de embeddings ===
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# === Banco vetorial (Chroma) ===
chroma_db = Chroma.from_documents(documentos_crud, embedding=embeddings)

# === Chatbot ===
print("💬 Olá! Eu sou o ChatMed — seu assistente virtual para agendamento de exames.\nDigite 'sair' para encerrar.\n")

while True:
    pergunta = input("Você: ")
    if pergunta.lower() == "sair":
        print("ChatMed: Obrigado por usar o ChatMed! Até a próxima.")
        break

    resultados = chroma_db.similarity_search(pergunta, k=1)
    if resultados:
        resposta = resultados[0].page_content
    else:
        resposta = "Desculpe, não encontrei nenhuma resposta sobre isso."
    
    print(f"ChatMed: {resposta}\n")
