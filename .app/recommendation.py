import pandas as pd
from random import choice, randint

RECEITAS_SAUDAVEIS = {
    "café": ["Iogurte com frutas", "Pão integral com ovo", "Smoothie verde"],
    "almoço": ["Salada com grão-de-bico", "Peixe grelhado com arroz integral", "Frango com legumes"],
    "jantar": ["Sopa de legumes", "Omelete com espinafre", "Macarrão integral com legumes"]
}

def recommend_diet(food_compositions):
    return {}  # placeholder se não houver lógica de substituição ainda

def gerar_matriz_dieta(alimentos):
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    matriz = []

    for dia in dias:
        cafe = choice(RECEITAS_SAUDAVEIS["café"])
        almoco = choice(RECEITAS_SAUDAVEIS["almoço"])
        jantar = choice(RECEITAS_SAUDAVEIS["jantar"])

        matriz.append({
            "Dia": dia,
            "Café da manhã": cafe,
            "Gramas Café": randint(150, 300),
            "Calorias Café": randint(200, 450),
            "Almoço": almoco,
            "Gramas Almoço": randint(400, 600),
            "Calorias Almoço": randint(500, 800),
            "Jantar": jantar,
            "Gramas Jantar": randint(300, 500),
            "Calorias Jantar": randint(400, 700),
        })

    return pd.DataFrame(matriz)
