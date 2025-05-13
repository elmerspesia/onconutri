import streamlit as st
from transformers import pipeline

# Carrega modelo open source de linguagem do Hugging Face
@st.cache_resource
def load_chat_model():
    return pipeline("text-generation", model="tiiuae/falcon-7b-instruct", tokenizer="tiiuae/falcon-7b-instruct")

def show_form():
    st.title("🩺 Formulário de Consulta")

    st.markdown("**Preencha o formulário abaixo com base nas respostas do paciente.**")

    idade = st.selectbox("Idade", ["<30", "30-45", "46-60", ">60"])
    genero = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"])
    tabagismo = st.selectbox("É fumante?", ["Nunca fumou", "Fumante ocasional", "Fumante regular", "Ex-fumante"])
    alcool = st.selectbox("Consumo de álcool", ["Nunca", "Social", "Frequente", "Abuso"])
    historico_familiar = st.selectbox("Histórico familiar de câncer?", ["Nenhum", "Sim - em parentes de primeiro grau", "Sim - em parentes distantes"])
    dieta = st.selectbox("Tipo de dieta predominante", ["Rica em vegetais e fibras", "Mista com carnes processadas", "Industrializada", "Vegetariana"])
    atividade_fisica = st.selectbox("Frequência de atividade física", ["Sedentário", "1-2 vezes/semana", "3+ vezes/semana"])
    exposicao = st.selectbox("Exposição a substâncias tóxicas (agrotóxicos, radiação, etc.)", ["Nenhuma", "Moderada", "Alta"])
    estresse = st.selectbox("Nível de estresse diário", ["Baixo", "Médio", "Alto"])

    if st.button("🔍 Processar Consulta"):
        respostas = f"""
        Paciente com idade {idade}, gênero {genero}, status de tabagismo: {tabagismo}, álcool: {alcool}, histórico familiar: {historico_familiar},
        dieta: {dieta}, atividade física: {atividade_fisica}, exposição a toxinas: {exposicao}, estresse: {estresse}.
        """

        model = load_chat_model()
        prompt = f"""
        Baseado no seguinte perfil do paciente, identifique os riscos mais prováveis de câncer, quais órgãos estão mais vulneráveis
        e proponha recomendações preventivas, incluindo dieta, acompanhamento clínico e hábitos de vida. Responda em português.
        
        Perfil do paciente:
        {respostas}
        """

        with st.spinner("🧠 Avaliando riscos e gerando recomendações..."):
            result = model(prompt, max_new_tokens=512, do_sample=True, temperature=0.7)
            st.subheader("📄 Resultado da Consulta Oncológica")
            st.write(result[0]["generated_text"])
