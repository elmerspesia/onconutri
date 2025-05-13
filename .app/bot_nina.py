import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_bot():
    return pipeline("text-generation", model="tiiuae/falcon-7b-instruct", max_new_tokens=100)

def bot_nina_ui():
    st.title("🤖 Nina - Assistente de IA")
    st.markdown("Converse com Nina sobre saúde, nutrição e prevenção ao câncer.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    prompt = st.text_input("Você:", key="user_input")

    if prompt:
        st.session_state.chat_history.append(("🧑 Você", prompt))
        with st.spinner("Nina está digitando..."):
            bot = load_bot()
            resposta = bot(f"Responda em português brasileiro: {prompt}")[0]['generated_text']
            resposta_limpa = resposta.split(":", 1)[-1].strip()
            st.session_state.chat_history.append(("🤖 Nina", resposta_limpa))

    for remetente, texto in reversed(st.session_state.chat_history):
        st.markdown(f"**{remetente}:** {texto}")
