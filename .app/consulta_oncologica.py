import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_generator():
    return pipeline("text2text-generation", model="google/flan-t5-base")

def gerar_diagnostico_ia(prompt):
    generator = load_generator()
    resposta = generator(prompt, max_length=512, do_sample=True)
    return resposta[0]['generated_text']

def montar_prompt(dados):
    prompt = f"""
Você é um médico oncologista especialista em prevenção de câncer. Analise o perfil do paciente abaixo com base em diretrizes científicas da OMS, INCA e literatura médica.

Perfil do paciente:
- Frequência alimentar: {dados['frequencia_alimentar']}
- Histórico familiar de câncer: {dados['historico_familiar']}
- Tipo de dieta: {dados['tipo_dieta']}
- Atividade física: {dados['atividade_fisica']}
- Exposição a toxinas: {dados['exposicao_toxinas']}
- Estresse diário: {dados['nivel_estresse']}

Com base nessas informações:
1. Calcule um score de risco de câncer (de 0.00 a 1.00).
2. Identifique possíveis tipos de câncer de risco elevado.
3. Forneça um diagnóstico preventivo e recomendações de mudança de estilo de vida para reduzir o risco.
Responda em português claro e acessível.
"""
    return prompt

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
            prompt = montar_prompt(dados)
            resposta = gerar_diagnostico_ia(prompt)

            st.success("✅ Consulta processada com sucesso.")

            st.subheader("📝 Resultado da Consulta Oncológica")

            # Score fictício extraído da IA (seria ideal extrair com expressão regular)
            score = "0.00"
            if "0." in resposta or "1.0" in resposta:
                import re
                encontrados = re.findall(r"\b0\.\d{2}|\b1\.00", resposta)
                if encontrados:
                    score = encontrados[0]

            st.markdown(f"📊 **Score de Propensão ao Câncer:** `{score}`")
            st.markdown("📄 **Diagnóstico e Recomendação:**")
            st.write(resposta)
