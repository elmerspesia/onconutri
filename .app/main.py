import streamlit as st
from PIL import Image
from io import BytesIO
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(__file__))

from food_detection import identificar_alimentos
from risco_alimentos import calcular_score, classificar_risco
from recommendation import gerar_dieta, mapa_beneficios
import consulta_oncologica

# --- Autenticação simples ---
def autenticar(usuario, senha):
    return usuario == "admin" and senha == "1234"

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if autenticar(usuario, senha):
            st.session_state.autenticado = True
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos")
    st.stop()

# --- Menu principal ---
st.sidebar.title("📋 Menu")
pagina = st.sidebar.selectbox("Escolha uma funcionalidade", [
    "Consulta por Imagem",
    "Consulta Oncológica com IA"
])

# --- Página: Consulta por Imagem ---
if pagina == "Consulta por Imagem":
    st.title("OncoPredix AI - Análise Oncológica Nutricional por Imagem")

    uploaded_files = st.file_uploader("Envie imagens de pratos alimentares", type=["jpg", "png"], accept_multiple_files=True)

    if uploaded_files:
        imagens = [Image.open(BytesIO(file.read())) for file in uploaded_files]
        df_alimentos = identificar_alimentos(imagens)

        if df_alimentos.empty:
            st.warning("Nenhum alimento reconhecido nas imagens enviadas. Tente novamente com outras imagens.")
        else:
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

# --- Página: Consulta Oncológica com IA ---
elif pagina == "Consulta Oncológica com IA":
    consulta_oncologica.main()
