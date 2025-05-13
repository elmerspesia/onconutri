from PIL import Image
import numpy as np
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import pandas as pd

# Carrega o modelo BLIP
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Mapeamento de alimentos e classificação
ALIMENTO_CLASSIFICACAO = {
    "carrot": "cenoura",
    "rice": "arroz",
    "beans": "feijão",
    "lettuce": "alface",
    "tomato": "tomate",
    "chicken": "frango",
    "beef": "carne bovina",
    "pork": "carne suína",
    "fish": "peixe",
    "egg": "ovo",
    "salad": "salada",
    "french fries": "batata frita",
    "bread": "pão",
    "pasta": "macarrão",
    "hamburger": "hambúrguer",
    "hot dog": "salsicha",
    "donut": "rosquinha",
    "pizza": "pizza",
    "chips": "batata chips"
}

CLASSIFICACAO_TIPO = {
    "cenoura": "natural",
    "arroz": "natural",
    "feijão": "natural",
    "alface": "natural",
    "tomate": "natural",
    "frango": "natural",
    "carne bovina": "natural",
    "carne suína": "natural",
    "peixe": "natural",
    "ovo": "natural",
    "salada": "natural",
    "pão": "processado",
    "macarrão": "processado",
    "batata frita": "ultraprocessado",
    "salsicha": "ultraprocessado",
    "hambúrguer": "ultraprocessado",
    "rosquinha": "ultraprocessado",
    "pizza": "ultraprocessado",
    "batata chips": "ultraprocessado"
}

@torch.no_grad()
def describe_image(img: Image.Image) -> str:
    inputs = processor(images=img, return_tensors="pt")
    out = blip_model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True).lower()
    return caption

def identificar_alimentos(imagens):
    resultados = []

    for imagem in imagens:
        legenda = describe_image(imagem)
        for palavra_en, alimento_pt in ALIMENTO_CLASSIFICACAO.items():
            if palavra_en in legenda:
                resultados.append({
                    "Alimento": alimento_pt,
                    "Classificação": CLASSIFICACAO_TIPO.get(alimento_pt, "desconhecido"),
                    "Legenda Detectada": legenda
                })

    return pd.DataFrame(resultados)
