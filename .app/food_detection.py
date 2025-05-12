from PIL import Image
import numpy as np
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# BLIP (image-to-text)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

@torch.no_grad()
def describe_crop(crop_img: Image.Image) -> str:
    inputs = processor(images=crop_img, return_tensors="pt")
    out = blip_model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption.strip()

# Tradução local (evita uso de API externa)
def translate_text(text):
    substitutions = {
        "plate of food": "prato de comida",
        "with": "com",
        "shrimp": "camarão",
        "meat": "carne",
        "vegetables": "vegetais",
        "a close up of": "uma imagem próxima de",
        "bowl": "tigela",
        "rice": "arroz",
        "leaf": "folha",
        "carrot": "cenoura",
        "piece": "pedaço",
        "and": "e",
        "a": "um",
    }
    for eng, pt in substitutions.items():
        text = text.replace(eng, pt)
    return text

def identify_foods(image: Image.Image, model):
    results = model.predict(source=np.array(image), save=False, verbose=False)
    result = results[0]

    food_data = []
    total_pixels = image.width * image.height

    if not hasattr(result, "boxes") or result.boxes is None:
        return [("não identificado", 1.0, 0.0)]

    for mask, box, conf in zip(result.masks.data, result.boxes.xyxy, result.boxes.conf):
        mask_np = mask.cpu().numpy().astype(np.uint8)
        pixels = np.sum(mask_np)
        percentage = pixels / total_pixels

        x1, y1, x2, y2 = map(int, box.tolist())
        cropped = image.crop((x1, y1, x2, y2))

        caption = describe_crop(cropped)
        label = translate_text(caption)

        food_data.append((label, percentage, float(conf)))

    if not food_data:
        food_data.append(("não identificado", 1.0, 0.0))

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
