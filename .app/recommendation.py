from collections import Counter, defaultdict

SUBSTITUTIONS = {
    "processed_meat": ["legumes", "tofu", "grilled chicken"],
    "fried_foods": ["baked potatoes", "steamed vegetables"],
    "sugary_foods": ["fruits", "unsweetened yogurt"],
    "red_meat": ["white_meat", "fish"],
    "unknown": ["vegetables", "fruits"]
}

CATEGORY_LABELS = {
    "processed_meat": ["pizza", "hot dog", "sandwich"],
    "fried_foods": ["fries"],
    "sugary_foods": ["cake", "doughnut"],
    "red_meat": ["steak", "beef"],
    "white_meat": ["chicken"],
    "vegetables": ["broccoli", "carrot", "tomato"],
    "fruits": ["apple", "banana", "orange"],
    "whole_grains": ["oats", "brown rice", "quinoa"],
    "legumes": ["lentils", "beans"],
    "fish": ["salmon", "tuna"]
}

def recommend_diet(food_compositions):
    food_counter = Counter()

    for comp in food_compositions:
        for food, _, _ in comp["foods"]:
            for category, members in CATEGORY_LABELS.items():
                if food in members:
                    food_counter[category] += 1
                    break

    recommendations = defaultdict(list)
    for category, count in food_counter.items():
        if category in SUBSTITUTIONS:
            recommendations[category] = {
                "current_count": count,
                "suggested_replacements": SUBSTITUTIONS[category]
            }

    return recommendations
