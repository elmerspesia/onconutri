import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_generator():
    return pipeline("text2text-generation", model="google/flan-t5-base")

def calcular_score(dados):
    score = 0
    pesos = {
        "frequencia_alimentar": {"Alta": 0.3, "Média": 0.15, "Baixa": 0.0},
        "historico_familiar": {
            "Sim - parentes de 1º grau": 0.3,
            "Sim - parentes de 2º grau": 0.15,
            "Não": 0.0
        },
        "tipo_dieta": {
            "Industrializada": 0.2,
            "Balanceada": 0.05,
            "Vegetariana": 0.0,
            "Outros": 0.1
        },
        "atividade_fisica": {
            "Sedentário": 0.2,
            "Moderado": 0.1,
            "Ativo": 0.0
        },
        "exposicao_toxinas": {
            "Alta": 0.2,
            "Moderada": 0.1,
            "Nenhuma": 0.0
        },
        "nivel_estresse": {
            "Alto": 0.1,
            "Médio": 0.05,
            "Baixo": 0.0
        }
    }

    for fator, valor in dados.items():
        score += pesos.get(fator, {}).get(valor, 0)

    return round(min(score, 1.0), 2)

def montar_prompt_ia(dados):
    respostas_texto = "\n".join([f"- {chave.replace('_', ' ').capitalize()}: {valor}" for chave, valor in dados.items()])

    prompt = (
        "Você é um oncologista especializado em prevenção oncogenital. "
        "Analisa o perfil do paciente utilizando as bases da OMS, INCA e literatura da área da saúde. "
        "Identifica variantes de risco relacionadas ao risco, identificando tipos perigosos de câncer. "
        "Responde com um português claro e acessível.\n\n"
        "Perfil do paciente:\n"
        f"{respostas_texto}"
    )
    return prompt

def gerar_resposta_ia(prompt):
    generator = load_generator()
    resposta = generator(prompt, max_length=512, do_sample=True)
    return resposta[0]['generated_text']

def show_form():
    st.header("🧬 Formulário de Consulta")

    frequencia_alimentar = st.selectbox("Frequência de alimentação processada:", ["Alta", "Média", "Baixa"])
    historico_familiar = st.selectbox("Histórico familiar de câncer:", ["Sim - parentes de 1º grau", "Sim - parentes de 2º grau", "Não"])
    tipo_dieta = st.selectbox("Tipo de dieta predominante", ["Industrializada", "Balanceada", "Vegetariana", "Outros"])
    atividade_fisica = st.selectbox("Frequência de atividade física", ["Sedentário", "Moderado", "Ativo"])
    exposicao_toxinas = st.selectbox("Exposição a toxinas (agrotóxicos, radiação)", ["Nenhuma", "Moderada", "Alta"])
    nivel_estresse = st.selectbox("Nível de estresse diário", ["Baixo", "Médio", "Alto"])

    if st.button("🔍 Processar Consulta"):
        with st.spinner("Processando consulta..."):
            dados = {
                "frequencia_alimentar": frequencia_alimentar,
                "historico_familiar": historico_familiar,
                "tipo_dieta": tipo_dieta,
                "atividade_fisica": atividade_fisica,
                "exposicao_toxinas": exposicao_toxinas,
                "nivel_estresse": nivel_estresse
            }

            score = calcular_score(dados)
            prompt = montar_prompt_ia(dados)
            resposta_ia = gerar_resposta_ia(prompt)

            st.success("✅ Consulta processada com sucesso.")
            st.subheader("📝 Resultado da Consulta Oncológica")
            st.markdown(f"📊 **Score de Propensão ao Câncer:** `{score}`")
            st.markdown("📄 **Diagnóstico e Recomendação:**")
            st.write(resposta_ia)
