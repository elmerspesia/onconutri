import streamlit as st
from transformers import pipeline

st.title("🧬 Consulta Oncológica com IA")

st.markdown("""
Este módulo permite que você faça uma pergunta relacionada à sua saúde oncológica ou hábitos alimentares e receba uma resposta gerada por IA em **português brasileiro**.
""")

prompt = st.text_area("Digite sua pergunta:")

if prompt:
    with st.spinner("Analisando com IA..."):
        # Simulação com pipeline de texto genérico da HuggingFace (substituível por modelo local open source em produção)
        gerador = pipeline("text-generation", model="tiiuae/falcon-7b-instruct", device_map="auto", max_new_tokens=256)
        resposta = gerador(f"Responda em português brasileiro: {prompt}", do_sample=True)[0]['generated_text']
        
        st.subheader("🗣️ Resposta da IA")
        st.write(resposta.split(":", 1)[-1].strip())
