from PIL import Image
import numpy as np

# COCO para alimentos adaptados
COCO_TO_FOOD = {
    37: "chicken",
    41: "tomato",
    56: "broccoli",
    57: "carrot",
    60: "doughnut",
    61: "cake",
    49: "orange",
    46: "banana",
    47: "apple",
    48: "sandwich",
    52: "hot dog",
    53: "pizza",
    44: "bottle",
    0: "unknown"
}

def preprocess_image(image):
    return np.array(image)

def identify_foods(image, predictor):
    inputs = preprocess_image(image)
    outputs = predictor(inputs)
    instances = outputs["instances"].to("cpu")

    masks = instances.pred_masks.numpy()
    classes = instances.pred_classes.numpy()
    scores = instances.scores.numpy()

    food_data = []
    total_pixels = masks[0].size if masks.shape[0] > 0 else 1

    for mask, cls_id, score in zip(masks, classes, scores):
        food = COCO_TO_FOOD.get(cls_id, "unknown")
        pixel_count = mask.sum()
        percentage = pixel_count / total_pixels
        food_data.append((food, percentage, score))

    return food_data

def process_uploaded_images(files, predictor):
    results = []
    for file in files:
        image = Image.open(file).convert("RGB")
        food_items = identify_foods(image, predictor)
        results.append({
            "filename": file.name,
            "foods": food_items,
            "image": image
        })
    return results
