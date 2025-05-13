import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_bot():
    return pipeline("text-generation", model="tiiuae/falcon-7b-instruct", max_new_tokens=256)

def show_bot():
    st.title("🤖 Chat com o Bot Nutricional Oncológico")
    st.markdown("Converse com uma IA sobre alimentação, saúde e prevenção ao câncer.")

    bot = load_bot()

    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []

    user_input = st.text_input("Digite sua pergunta:")

    if user_input:
        st.session_state.mensagens.append(("Usuário", user_input))
        with st.spinner("Pensando..."):
            resposta = bot(f"Responda em português brasileiro: {user_input}")[0]['generated_text']
            resposta_limpa = resposta.split(":", 1)[-1].strip()
            st.session_state.mensagens.append(("Bot", resposta_limpa))

    for remetente, texto in reversed(st.session_state.mensagens):
        if remetente == "Usuário":
            st.markdown(f"**👤 Você:** {texto}")
        else:
            st.markdown(f"**🤖 Bot:** {texto}")
