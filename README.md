# 🩺 ChatMed — Sistema de Agendamento e Consulta Médica

## 👥 Integrantes
- **Rafael Tavares Santos** | RM: 563487  
- **Gabriel Oliveira Amaral** | RM: 563872  
- **Felipe Yamagushi Mesquita** | RM: 556170  

---

## 📋 Descrição do Projeto
O **ChatMed** é um assistente virtual em **Python** que permite ao usuário **agendar, visualizar, atualizar e desmarcar consultas médicas** de forma interativa.  
O sistema utiliza o modelo de **embeddings da Hugging Face** e o **banco vetorial Chroma** para compreender perguntas e responder de forma contextualizada.

---

## ⚙️ Tecnologias Utilizadas
- 🐍 **Python 3.10+**
- 🧩 **LangChain**
- 🤗 **Hugging Face Embeddings**
- 🗃️ **ChromaDB**

---

## 🧠 Funcionalidades Principais

| Função | Descrição |
|--------|------------|
| 🗓️ **Agendar exame** | Permite escolher **dia, horário, exame e médico** disponíveis. |
| 📋 **Consultar agendamentos** | Exibe todos os exames marcados com detalhes. |
| ✏️ **Atualizar agendamento** | Permite editar informações de um agendamento existente. |
| ❌ **Desmarcar agendamento** | Remove um exame agendado. |
| 💬 **Chat inteligente** | O chatbot responde dúvidas sobre o sistema (ex: “como agendar um exame?”). |

---

## 🧩 Estrutura do Código

- **menu:**  
  Armazena os horários, dias, exames, médicos e os agendamentos realizados.  

- **Funções principais:**  
  - `forca_opcao()` → Garante que o usuário escolha apenas opções válidas.  
  - `exames_marcados()` → Exibe os agendamentos existentes.  
  - `agendamento()` → Cria um novo agendamento.  
  - `desmarcar_agendamento()` → Cancela um agendamento.  
  - `atualizar_agendamento()` → Edita dados de um agendamento existente.  

- **opcoes:**  
  Dicionário que mapeia palavras-chave digitadas pelo usuário (“agendar”, “cancelar”, “ver”, etc.) às funções correspondentes.  

- **documentos_crud:**  
  Base de conhecimento usada pelo chatbot para responder dúvidas gerais.  

- **embeddings e chroma_db:**  
  Criam a base vetorial de respostas inteligentes usando o modelo `all-MiniLM-L6-v2`.

---

## 💬 Exemplo de Uso

```bash
Olá! Eu sou o ChatMed — seu assistente virtual para agendamento de exames.
Digite 'sair' para encerrar.

Você: quero agendar um exame
ChatMed: Escolha o Dia desejado:
11/11/2025
12/11/2025
13/11/2025
...
-> 12/11/2025
