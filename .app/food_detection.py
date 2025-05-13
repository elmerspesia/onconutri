from PIL import Image
import numpy as np
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Modelos
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Dicionário de mapeamento de alimentos para classes padronizadas (expansível)
ALIMENTO_PADRAO = {
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
    "pasta": "macarrão"
}

@torch.no_grad()
def describe_crop(crop_img: Image.Image) -> str:
    inputs = processor(images=crop_img, return_tensors="pt")
    out = blip_model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True).lower()
    return caption

def padronizar_alimento(descricao):
    for chave, valor in ALIMENTO_PADRAO.items():
        if chave in descricao:
            return valor
    return descricao  # mantém original se não mapear

def identify_foods(image: Image.Image, model):
    results = model.predict(source=np.array(image), save=False, verbose=False)
    result = results[0]

    food_data = []
    total_pixels = image.width * image.height

    if not hasattr(result, "boxes") or result.boxes is None:
        return [("não identificado", 1.0, 0.0)]

    for mask, box, conf in zip(result.masks.data, result.boxes.xyxy, result.boxes.conf):
        pixels = np.sum(mask.cpu().numpy())
        percent = pixels / total_pixels

        x1, y1, x2, y2 = map(int, box.tolist())
        cropped = image.crop((x1, y1, x2, y2))

        descricao = describe_crop(cropped)
        alimento = padronizar_alimento(descricao)

        food_data.append((alimento, percent, float(conf)))

    return food_data

def process_uploaded_images(files, model):
    results = []
    for file in files:
        image = Image.open(file).convert("RGB")
        food_items = identify_foods(image, model)
        results.append({
            "filename": file.name,
            "foods": food_items,
            "image": image
        })
    return results
