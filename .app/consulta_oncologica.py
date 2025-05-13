import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_chat_model():
    return pipeline("text2text-generation", model="google/flan-t5-base")

@st.cache_resource
def load_translator():
    return pipeline("translation", model="Helsinki-NLP/opus-mt-en-pt")

def show_form():
    st.title("🩺 Formulário de Consulta Oncológica")

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
        with st.spinner("Processando avaliação com IA..."):

            # Engenharia de Prompt com CAG + DAG + RAG
            contexto_medico = (
                "Você é um assistente médico especializado em oncologia preventiva. "
                "Analise o perfil abaixo de acordo com estudos da OMS, INCA, PubMed e NCCN."
            )

            dados_struct = f"""
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

            prompt = (
                f"{contexto_medico}\n\n"
                f"Paciente:\n{dados_struct}\n\n"
                "Avalie em português:\n"
                "- O tipo mais provável de câncer com base nesse perfil\n"
                "- Um score numérico de propensão ao câncer (de 0.00 a 1.00)\n"
                "- Recomendações detalhadas de hábitos que reduzam esse risco\n"
                "- Diagnóstico preventivo completo\n\n"
                "Responda apenas em português, com linguagem médica clara e objetiva."
            )

            try:
                modelo = load_chat_model()
                saida = modelo(prompt, max_new_tokens=512)[0]['generated_text']

                tradutor = load_translator()
                traducao = tradutor(saida, max_length=512)[0]['translation_text']

                # Score extraído por regex ou heurística (ajustável)
                import re
                score_match = re.search(r'([0-1]\.\d{1,2})', traducao)
                score = float(score_match.group(1)) if score_match else 0.0

                st.success("Consulta processada com sucesso.")
                st.subheader("📄 Resultado da Consulta Oncológica")
                st.markdown(f"**📊 Score de propensão ao câncer:** `{score:.2f}`")
                st.markdown(f"**🩺 Diagnóstico e Recomendação:**\n\n{traducao}")

            except Exception as e:
                st.error("❌ Erro ao processar a consulta.")
                st.exception(e)
