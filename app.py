import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# --------------------------------------------------
# CONFIGURAÇÃO
# --------------------------------------------------

st.set_page_config(
    page_title="Chatbot Groq",
    page_icon="🤖",
    layout="centered"
)

# Carrega as variáveis do arquivo .env
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

# --------------------------------------------------
# TÍTULO
# --------------------------------------------------

st.title("🤖 Chatbot Groq")
st.caption("Faça uma pergunta e converse com a inteligência artificial.")

# --------------------------------------------------
# VERIFICA A CHAVE DA API
# --------------------------------------------------

if not API_KEY:
    st.error("A chave GROQ_API_KEY não foi encontrada no arquivo .env.")
    st.stop()

# Cria o cliente Groq
client = Groq(api_key=API_KEY)

# --------------------------------------------------
# HISTÓRICO DA CONVERSA
# --------------------------------------------------

if "historico" not in st.session_state:
    st.session_state.historico = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Configurações")

    st.write("Chatbot desenvolvido com:")
    st.write("🐍 Python")
    st.write("🎈 Streamlit")
    st.write("🤖 Groq")

    st.divider()

    if st.button("🗑️ Limpar conversa"):
        st.session_state.historico = []
        st.rerun()

# --------------------------------------------------
# MOSTRA O HISTÓRICO
# --------------------------------------------------

for mensagem in st.session_state.historico:

    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

# --------------------------------------------------
# CAMPO DE PERGUNTA
# --------------------------------------------------

pergunta = st.chat_input("Digite sua pergunta...")

if pergunta:

    # Salva pergunta do usuário
    st.session_state.historico.append({
        "role": "user",
        "content": pergunta
    })

    # Mostra pergunta
    with st.chat_message("user"):
        st.markdown(pergunta)

    # --------------------------------------------------
    # RESPOSTA DA IA
    # --------------------------------------------------

    try:

        with st.chat_message("assistant"):

            with st.spinner("Pensando..."):

                resposta = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=st.session_state.historico
                )

                texto = resposta.choices[0].message.content

                st.markdown(texto)

        # Salva resposta no histórico
        st.session_state.historico.append({
            "role": "assistant",
            "content": texto
        })

    except Exception as erro:
        st.error(f"Erro ao gerar resposta: {erro}")