import pandas as pd

def calcular_score(df_alimentos):
    pesos = {
        "natural": 0,
        "processado": 1,
        "ultraprocessado": 3
    }
    df_alimentos["Peso"] = df_alimentos["Classificação"].map(pesos)
    score = df_alimentos["Peso"].sum()
    return score / max(1, len(df_alimentos))

def classificar_risco(score):
    if score < 0.5:
        return "Baixo"
    elif score < 1.5:
        return "Moderado"
    else:
        return "Alto"
