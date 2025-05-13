from PIL import Image
import numpy as np
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import pandas as pd

# Carrega o modelo BLIP para legendas de imagens
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Mapeamento de alimentos e classificação
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
def describe_crop(crop_img: Image.Image) -> str:
    inputs = processor(images=crop_img, return_tensors="pt")
    out = blip_model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True).lower()
    return caption

def identificar_alimentos(imagens):
    resultados = []
    for imagem in imagens:
        descricao = describe_crop(imagem)
        alimento_detectado = None
        for item in ALIMENTO_CLASSIFICACAO:
            if item in descricao:
                alimento_detectado = item
                break
        if alimento_detectado:
            resultados.append({
                "Alimento": alimento_detectado,
                "Classificação": ALIMENTO_CLASSIFICACAO[alimento_detectado]
            })
    return pd.DataFrame(resultados)
