import pandas as pd
import streamlit as st

def show_ranking():
    st.title("📈 Ranking de Alimentos Industrializados e Riscos Oncológicos")

    dados = [
        {"Alimento Industrializado": "Salsicha", "Tipo de Câncer Associado": "Colorretal"},
        {"Alimento Industrializado": "Presunto", "Tipo de Câncer Associado": "Estômago"},
        {"Alimento Industrializado": "Mortadela", "Tipo de Câncer Associado": "Esôfago"},
        {"Alimento Industrializado": "Refrigerante", "Tipo de Câncer Associado": "Pâncreas"},
        {"Alimento Industrializado": "Batata frita de pacote", "Tipo de Câncer Associado": "Mama"},
        {"Alimento Industrializado": "Bolacha recheada", "Tipo de Câncer Associado": "Colorretal"},
        {"Alimento Industrializado": "Cereais açucarados", "Tipo de Câncer Associado": "Fígado"},
        {"Alimento Industrializado": "Nuggets de frango", "Tipo de Câncer Associado": "Próstata"},
        {"Alimento Industrializado": "Macarrão instantâneo", "Tipo de Câncer Associado": "Estômago"},
        {"Alimento Industrializado": "Bacon", "Tipo de Câncer Associado": "Colorretal"},
        {"Alimento Industrializado": "Embutidos (geral)", "Tipo de Câncer Associado": "Colorretal"},
        {"Alimento Industrializado": "Alimentos com corantes artificiais", "Tipo de Câncer Associado": "Vários tipos"},
    ]

    df = pd.DataFrame(dados)
    st.dataframe(df, use_container_width=True)
