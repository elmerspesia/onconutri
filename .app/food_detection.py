from PIL import Image
import numpy as np
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import pandas as pd

# Modelo BLIP
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Mapeamento e classificação
ALIMENTO_CLASSIFICACAO = {
    "cenoura": "natural",
    "arroz": "natural",
    "feijão": "natural",
    "alface": "natural",
    "tomate": "natural",
    "frango": "natural",
    "carne bovina": "natural",
    "peixe": "natural",
    "ovo": "natural",
    "pão": "processado",
    "macarrão": "processado",
    "salsicha": "ultraprocessado",
    "presunto": "ultraprocessado",
    "mortadela": "ultraprocessado",
    "refrigerante": "ultraprocessado",
    "batata frita": "ultraprocessado",
    "bolacha recheada": "ultraprocessado",
    "cereais açucarados": "ultraprocessado",
    "nuggets": "ultraprocessado",
    "macarrão instantâneo": "ultraprocessado",
    "bacon": "ultraprocessado"
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
        encontrados = []
        for alimento in ALIMENTO_CLASSIFICACAO:
            if alimento in legenda:
                encontrados.append((alimento, ALIMENTO_CLASSIFICACAO[alimento]))
        for nome, tipo in encontrados:
            resultados.append({"Alimento": nome, "Classificação": tipo})

    return pd.DataFrame(resultados)
