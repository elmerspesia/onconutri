from PIL import Image
import numpy as np

# Ajuste para todos os alimentos do seu modelo (exemplo ampliável)
YOLO_CLASS_TO_FOOD = {
    0: "apple",
    1: "banana",
    2: "cake",
    3: "chicken",
    4: "fries",
    5: "pizza",
    6: "broccoli",
    7: "carrot",
    8: "hot dog",
    9: "sandwich",
    10: "orange",
    11: "tomato",
    12: "doughnut"
}

def identify_foods(image, model):
    results = model.predict(source=np.array(image), save=False, verbose=False)
    result = results[0]

    food_data = []
    total_pixels = image.width * image.height

    if not hasattr(result, "boxes") or result.boxes is None:
        return [("unknown", 1.0, 0.0)]

    for box, mask, cls, conf in zip(result.boxes.xyxy, result.masks.data, result.boxes.cls, result.boxes.conf):
        mask_np = mask.cpu().numpy().astype(np.uint8)
        pixels = np.sum(mask_np)
        percentage = pixels / total_pixels

        label = YOLO_CLASS_TO_FOOD.get(int(cls), "unknown")
        food_data.append((label, percentage, float(conf)))

    if not food_data:
        food_data.append(("unknown", 1.0, 0.0))

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
