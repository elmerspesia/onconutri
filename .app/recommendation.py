import pandas as pd
import streamlit as st
import graphviz

def gerar_dieta(df):
    substituicoes = {
        "salsicha": "grão-de-bico",
        "presunto": "peito de frango",
        "mortadela": "tofu",
        "refrigerante": "água com limão",
        "batata frita": "batata doce assada",
        "bolacha recheada": "fruta fresca",
        "cereais açucarados": "aveia",
        "nuggets": "frango grelhado",
        "macarrão instantâneo": "arroz integral",
        "bacon": "ovo cozido"
    }

    nova_dieta = []
    for alimento in df["Alimento"]:
        novo = substituicoes.get(alimento, alimento)
        nova_dieta.append(novo)
    return pd.DataFrame({"Dieta Recomendada": nova_dieta})

def mapa_beneficios():
    g = graphviz.Digraph()
    g.node("Dieta Saudável")
    g.edge("Dieta Saudável", "Redução de inflamações")
    g.edge("Dieta Saudável", "Melhoria da imunidade")
    g.edge("Dieta Saudável", "Redução do risco de câncer")
    g.edge("Dieta Saudável", "Controle de peso")
    g.edge("Dieta Saudável", "Saúde cardiovascular")
    st.graphviz_chart(g)
