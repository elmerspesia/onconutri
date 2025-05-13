import pandas as pd
from random import choice

RECEITAS_SAUDAVEIS = {
    "café": ["Iogurte com frutas", "Pão integral com ovo", "Smoothie verde"],
    "almoço": ["Salada com grão-de-bico", "Peixe grelhado com arroz integral", "Frango com legumes"],
    "jantar": ["Sopa de legumes", "Omelete com espinafre", "Macarrão integral com legumes"]
}

def recommend_diet(food_compositions):
    # Lógica de substituição opcional (placeholder funcional)
    return {}

def gerar_matriz_dieta(alimentos):
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    matriz = []

    for dia in dias:
        matriz.append({
            "Dia": dia,
            "Café da manhã": choice(RECEITAS_SAUDAVEIS["café"]),
            "Almoço": choice(RECEITAS_SAUDAVEIS["almoço"]),
            "Jantar": choice(RECEITAS_SAUDAVEIS["jantar"])
        })

    return pd.DataFrame(matriz)
