import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_chat_model():
    # Modelo mais leve e rápido (não precisa de API key)
    return pipeline("text2text-generation", model="google/flan-t5-large")

def show_form():
    st.title("🩺 Formulário de Consulta Oncológica")

    st.markdown("**Responda ao formulário com informações do paciente.**")

    idade = st.selectbox("Idade", ["<30", "30-45", "46-60", ">60"])
    genero = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"])
    tabagismo = st.selectbox("É fumante?", ["Nunca fumou", "Fumante ocasional", "Fumante regular", "Ex-fumante"])
    alcool = st.selectbox("Consumo de álcool", ["Nunca", "Social", "Frequente", "Abuso"])
    historico_familiar = st.selectbox("Histórico familiar de câncer?", ["Nenhum", "Sim - parentes de 1º grau", "Sim - parentes distantes"])
    dieta = st.selectbox("Tipo de dieta predominante", ["Rica em vegetais e fibras", "Mista com carnes processadas", "Industrializada", "Vegetariana"])
    atividade_fisica = st.selectbox("Frequência de atividade física", ["Sedentário", "1-2x por semana", "3+ vezes/semana"])
    exposicao = st.selectbox("Exposição a toxinas (agrotóxicos, radiação)", ["Nenhuma", "Moderada", "Alta"])
    estresse = st.selectbox("Nível de estresse diário", ["Baixo", "Médio", "Alto"])

    if st.button("🔍 Processar Consulta"):
        respostas = f"""
        Idade: {idade}, Gênero: {genero}, Tabagismo: {tabagismo}, Álcool: {alcool},
        Histórico familiar: {historico_familiar}, Dieta: {dieta},
        Atividade física: {atividade_fisica}, Exposição: {exposicao}, Estresse: {estresse}.
        """

        prompt = f"""
        Com base neste perfil do paciente, avalie o risco de câncer mais provável e recomende estratégias de prevenção alimentar e de estilo de vida.
        Responda em português e de forma objetiva. Perfil: {respostas}
        """

        st.subheader("📄 Resultado da Consulta Oncológica")
        try:
            modelo = load_chat_model()
            resultado = modelo(prompt, max_new_tokens=300)[0]['generated_text']
            st.success("✅ Consulta processada com sucesso.")
            st.markdown(f"**📋 Diagnóstico e Recomendação:**\n\n{resultado}")
        except Exception as e:
            st.error("❌ Ocorreu um erro ao processar a consulta. Por favor, tente novamente.")
            st.exception(e)
