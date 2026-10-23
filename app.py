import streamlit as st
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="Meu Chat IA",
    page_icon="🤖"
)

st.title("🤖 Meu Chat IA")
st.caption("Powered by Groq")

# Histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

# Conectar ao Groq
try:
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
except Exception:
    st.error(
        "Não encontrei a chave GROQ_API_KEY. "
        "Confira o arquivo .streamlit/secrets.toml."
    )
    st.stop()

# Barra lateral
with st.sidebar:
    st.header("⚙️ Configurações")

    if st.button("🗑️ Nova conversa"):
        st.session_state.messages = []
        st.rerun()

# Mostrar mensagens anteriores
for mensagem in st.session_state.messages:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

# Campo para enviar mensagens
if pergunta := st.chat_input("Digite sua mensagem..."):

    st.session_state.messages.append({
        "role": "user",
        "content": pergunta
    })

    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Groq está pensando..."):

                resposta = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Você é um assistente amigável. "
                                "Responda em português brasileiro "
                                "e explique assuntos de forma simples."
                            )
                        },
                        *st.session_state.messages
                    ]
                )

                texto = resposta.choices[0].message.content

            st.markdown(texto)

            st.session_state.messages.append({
                "role": "assistant",
                "content": texto
            })

        except OpenAIError as erro:
            st.error(f"Erro na API do Groq: {erro}")