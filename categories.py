"""Auto-categorization of shopping items by keyword matching."""

CATEGORIES: dict[str, list[str]] = {
    "🥬 Produce": [
        "apple", "apples", "banana", "bananas", "orange", "oranges",
        "grape", "grapes", "lemon", "lemons", "lime", "limes",
        "berry", "berries", "strawberry", "strawberries", "blueberry", "blueberries",
        "mango", "mangos", "pineapple", "watermelon", "avocado", "avocados",
        "tomato", "tomatoes", "lettuce", "spinach", "broccoli", "cucumber",
        "cucumbers", "carrot", "carrots", "onion", "onions", "garlic",
        "potato", "potatoes", "sweet potato", "celery", "pepper", "peppers",
        "mushroom", "mushrooms", "corn", "pea", "peas", "bean", "beans",
        "zucchini", "squash", "kale", "cabbage", "arugula", "radish",
        "herb", "herbs", "parsley", "cilantro", "basil", "mint", "dill",
    ],
    "🧀 Dairy": [
        "milk", "cheese", "cheeses", "yogurt", "yoghurt", "butter",
        "cream", "sour cream", "cream cheese", "whipping cream",
        "kefir", "cottage cheese", "ricotta", "mozzarella", "parmesan",
        "cheddar", "swiss cheese", "feta", "gouda",
    ],
    "🥩 Meat": [
        "chicken", "beef", "pork", "steak", "bacon", "ham",
        "turkey", "sausage", "sausages", "ground beef", "ground pork",
        "lamb", "fish", "salmon", "tuna", "shrimp", "prawn",
        "prawns", "cod", "tilapia", "anchovy", "anchovies",
        "prosciutto", "salami", "pepperoni", "deli", "bacon",
    ],
    "🍞 Bakery": [
        "bread", "buns", "bagel", "bagels", "croissant", "croissants",
        "roll", "rolls", "pita", "tortilla", "tortillas", "naan",
        "muffin", "muffins", "cake", "pie", "donut", "donuts",
        "baguette", "english muffin", "pumpernickel", "rye",
    ],
    "🥫 Pantry": [
        "pasta", "rice", "flour", "sugar", "salt", "oil", "olive oil",
        "vinegar", "ketchup", "mustard", "mayo", "mayonnaise",
        "soy sauce", "honey", "jam", "jelly", "peanut butter",
        "almond butter", "chocolate", "cereal", "cracker", "crackers",
        "canned", "sauce", "salsa", "beans", "lentils", "quinoa",
        "oats", "oatmeal", "spice", "spices", "ginger", "vanilla",
        "chili", "pepper", "cumin", "paprika", "cinnamon", "nutmeg",
        "sauce", "tomato sauce", "pasta sauce", "olive", "olives",
        "pickle", "pickles", "capers", "corn", "tortilla chips", "chips",
        "snack", "snacks", "pretzel", "pretzels", "popcorn",
    ],
    "🥤 Drinks": [
        "water", "juice", "soda", "cola", "coffee", "tea",
        "beer", "wine", "whiskey", "vodka", "rum", "tequila",
        "champagne", "prosecco", "sparkling water", "energy drink",
        "milk", "almond milk", "oat milk", "coconut milk",
    ],
    "🚿 Bathroom": [
        "toothpaste", "toothbrush", "shampoo", "conditioner",
        "body wash", "soap", "deodorant", "razor", "razors",
        "shaving cream", "lotion", "moisturizer", "makeup",
        "cotton swab", "cotton swabs", "tissue", "tissues",
        "sanitary", "tampon", "tampons", "pad", "pads",
        "floss", "mouthwash", "hand sanitizer", "perfume",
        "cologne", "nail polish", "hair spray",
    ],
    "🧹 Household": [
        "toilet paper", "paper towel", "paper towels", "napkin", "napkins",
        "dish soap", "dishwasher", "bleach", "detergent", "fabric softener",
        "trash bag", "trash bags", "aluminum foil", "plastic wrap",
        "ziploc", "sponge", "sponges", "broom", "mop",
        "air freshener", "candle", "candles", "battery", "batteries",
        "light bulb", "light bulbs", "glue", "tape", "rubber band",
        "freezer bag", "freezer bags", "cling wrap", "cleaning",
    ],
    "🍿 Snacks": [
        "chips", "crisps", "popcorn", "candy", "gum", "mints",
        "chocolate", "cookies", "brownies", "granola bar", "granola bars",
        "trail mix", "nuts", "pretzel", "pretzels", "dried fruit",
        "jerky", "beef jerky", "crackers", "chips", "nachos",
    ],
    "📦 Other": [],
}

# Build a reverse lookup: keyword -> category
_KEYWORD_MAP: dict[str, str] = {}
for _category, _keywords in CATEGORIES.items():
    for _kw in _keywords:
        _KEYWORD_MAP[_kw] = _category


def guess_category(item_name: str) -> str:
    """Return the best category for an item name by keyword matching.

    Uses a two-pass strategy:
    1. Check if any keyword is contained in the item name (substring match).
    2. If no match, check if any keyword is contained in the keyword list (item is a substring of a keyword).
    Falls back to '📦 Other'.
    """
    name = item_name.strip().lower()

    # Pass 1: keyword in item name
    for kw, cat in _KEYWORD_MAP.items():
        if kw in name:
            return cat

    # Pass 2: item name is a substring of a keyword
    for kw, cat in _KEYWORD_MAP.items():
        if name in kw and len(name) >= 3:
            return cat

    return "📦 Other"
