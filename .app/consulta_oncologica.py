import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_chat_model():
    try:
        return pipeline("text2text-generation", model="google/flan-t5-base")
    except Exception as e:
        st.error("❌ Erro ao carregar modelo de IA. Verifique sua conexão ou tente novamente mais tarde.")
        raise e

def show_form():
    st.title("🩺 Formulário de Consulta Oncológica")

    st.markdown("Preencha o formulário abaixo para avaliar riscos potenciais de câncer e obter recomendações preventivas:")

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
        Com base neste perfil do paciente, avalie em português o risco mais provável de desenvolvimento de câncer e recomende estratégias preventivas nutricionais e comportamentais.
        Perfil: {respostas}
        """

        st.subheader("📄 Resultado da Consulta Oncológica")

        try:
            modelo = load_chat_model()
            resultado = modelo(prompt, max_new_tokens=256)[0]['generated_text']
            st.success("✅ Consulta processada com sucesso.")
            st.markdown(f"**📋 Diagnóstico e Recomendação:**\n\n{resultado}")
        except Exception as e:
            st.error("❌ Não foi possível gerar a recomendação da IA no momento.")
            st.exception(e)
