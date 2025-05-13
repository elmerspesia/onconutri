import streamlit as st
from PIL import Image
from io import BytesIO
import pandas as pd
from food_detection import identificar_alimentos
from risco_alimentos import calcular_score, classificar_risco
from recommendation import gerar_dieta, mapa_beneficios

st.set_page_config(layout="wide")
st.title("OncoPredix AI - Análise Oncológica Nutricional por Imagem")

uploaded_files = st.file_uploader("Envie imagens de pratos alimentares", type=["jpg", "png"], accept_multiple_files=True)

if uploaded_files:
    imagens = [Image.open(BytesIO(file.read())) for file in uploaded_files]
    df_alimentos = identificar_alimentos(imagens)

    st.subheader("🍽️ Alimentos Identificados")
    st.dataframe(df_alimentos)

    score = calcular_score(df_alimentos)
    risco = classificar_risco(score)

    st.subheader("🎯 Score de Propensão ao Câncer")
    st.metric("Score", f"{score:.2f}")
    st.write(f"Nível de risco: **{risco}**")

    st.subheader("🥗 Dieta Recomendada")
    dieta_df = gerar_dieta(df_alimentos)
    st.dataframe(dieta_df)

    st.subheader("🧠 Benefícios da Nova Dieta (Mapa Mental)")
    mapa_beneficios()
