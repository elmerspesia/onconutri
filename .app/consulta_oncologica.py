import streamlit as st
from transformers import pipeline
import re

# Cacheia o carregamento do modelo de IA
@st.cache_resource
def load_chat_model():
    return pipeline("text2text-generation", model="google/flan-t5-base")

# Função principal do formulário de consulta médica oncológica
def show_form():
    st.title("🩺 Formulário de Consulta Oncológica")

    # Coleta de informações do paciente
    idade = st.selectbox("Idade", ["<30", "30-45", "46-60", ">60"])
    genero = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"])
    tabagismo = st.selectbox("É fumante?", ["Nunca fumou", "Fumante ocasional", "Fumante regular", "Ex-fumante"])
    alcool = st.selectbox("Consumo de álcool", ["Nunca", "Social", "Frequente", "Abuso"])
    historico_familiar = st.selectbox("Histórico familiar de câncer?", ["Nenhum", "Sim - parentes de 1º grau", "Sim - parentes distantes"])
    dieta = st.selectbox("Tipo de dieta predominante", ["Rica em vegetais e fibras", "Mista com carnes processadas", "Industrializada", "Vegetariana"])
    atividade_fisica = st.selectbox("Frequência de atividade física", ["Sedentário", "1-2x por semana", "3+ vezes/semana"])
    exposicao = st.selectbox("Exposição a toxinas (agrotóxicos, radiação)", ["Nenhuma", "Moderada", "Alta"])
    estresse = st.selectbox("Nível de estresse diário", ["Baixo", "Médio", "Alto"])

    # Botão para processar a IA
    if st.button("🔍 Processar Consulta"):
        with st.spinner("Processando avaliação com IA..."):

            # Prompt em português nativo com Engenharia de Prompt para CAG + RAG
            contexto = (
                "Você é um médico oncologista com conhecimento em guidelines da OMS, INCA, PubMed e literatura científica. "
                "Analise o seguinte perfil de paciente e forneça:\n"
                "- O(s) tipo(s) mais provável(eis) de câncer com base nos fatores de risco\n"
                "- Um score de propensão oncológica de 0.00 a 1.00\n"
                "- Recomendações preventivas baseadas em evidências\n"
                "- Diagnóstico e orientação clínica em linguagem acessível\n\n"
            )

            respostas = f"""
            Idade: {idade}
            Gênero: {genero}
            Tabagismo: {tabagismo}
            Álcool: {alcool}
            Histórico familiar: {historico_familiar}
            Dieta: {dieta}
            Atividade física: {atividade_fisica}
            Exposição a toxinas: {exposicao}
            Estresse: {estresse}
            """

            prompt = contexto + "Perfil do paciente:\n" + respostas

            try:
                modelo = load_chat_model()
                resultado = modelo(prompt, max_new_tokens=512)[0]['generated_text']

                # Tenta extrair o score do texto
                score_match = re.search(r'([0-1]\.\d{1,2})', resultado)
                score = float(score_match.group(1)) if score_match else 0.0

                # Exibição
                st.success("✅ Consulta processada com sucesso.")
                st.subheader("📝 Resultado da Consulta Oncológica")
                st.markdown(f"**📊 Score de Propensão ao Câncer:** `{score:.2f}`")
                st.markdown(f"**📄 Diagnóstico e Recomendação:**\n\n{resultado}")

            except Exception as e:
                st.error("❌ Erro ao processar a IA.")
                st.exception(e)
