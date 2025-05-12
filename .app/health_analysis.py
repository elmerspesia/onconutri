import numpy as np

RISK_FACTORS = {
    "red_meat": 0.7,
    "processed_meat": 0.9,
    "vegetables": -0.6,
    "fruits": -0.5,
    "whole_grains": -0.4,
    "sugary_foods": 0.3,
    "fried_foods": 0.4
}

FOOD_CATEGORY_MAP = {
    "chicken": "white_meat",
    "tomato": "vegetables",
    "broccoli": "vegetables",
    "carrot": "vegetables",
    "cake": "sugary_foods",
    "pizza": "processed_meat",
    "hot dog": "processed_meat",
    "sandwich": "processed_meat",
    "apple": "fruits",
    "orange": "fruits",
    "banana": "fruits",
    "doughnut": "sugary_foods",
    "fries": "fried_foods",
    "unknown": "unknown"
}

def calculate_cancer_risk(food_composition):
    score = 0.0
    for food, percentage, _ in food_composition:
        category = FOOD_CATEGORY_MAP.get(food, "unknown")
        risk = RISK_FACTORS.get(category, 0.0)
        score += risk * percentage
    return round(min(max(score, 0), 1), 2)

def estimate_lifespan_gain(food_compositions):
    avg_risk = np.mean([calculate_cancer_risk(comp["foods"]) for comp in food_compositions])
    if avg_risk < 0.2:
        gain_years = 5
    elif avg_risk < 0.4:
        gain_years = 3
    elif avg_risk < 0.6:
        gain_years = 1.5
    else:
        gain_years = 0.5

    return gain_years, avg_risk
