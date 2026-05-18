PRODUCTS = {
    "plastic bag": [
        "Jute bag - 30 to 80 rupees at any Indian market or Fabindia",
        "Cotton tote bag - 50 to 150 rupees The Better India Store",
        "Cloth bag - 20 to 40 rupees at local market",
    ],
    "plastic bottle": [
        "Steel water bottle - 250 to 600 rupees Milton or Cello brand",
        "Copper bottle - 300 to 800 rupees also has health benefits",
        "Glass bottle - 150 to 400 rupees Borosil brand",
    ],
    "toothbrush": [
        "Bamboo toothbrush - 40 to 120 rupees available on Amazon India",
        "Neem datun twig - 5 to 15 rupees traditional and biodegradable",
    ],
    "soap": [
        "Khadi Natural soap bar - 50 to 120 rupees zero plastic packaging",
        "Medimix Ayurvedic bar - 30 to 60 rupees minimal packaging",
    ],
    "straw": [
        "Steel straw set - 100 to 200 rupees for 4 straws with brush",
        "Bamboo straw - 50 to 100 rupees biodegradable",
    ],
    "detergent": [
        "Soap nuts reetha - 100 to 200 rupees per kg 100 percent natural",
        "Ghadi detergent bar - 15 to 30 rupees minimal packaging",
    ],
    "bag": [
        "Jute bag - 30 to 80 rupees at any Indian market",
        "Cotton tote bag - 50 to 150 rupees reusable for years",
    ],
    "bottle": [
        "Steel water bottle - 250 to 600 rupees Milton or Cello brand",
        "Copper bottle - 300 to 800 rupees also has health benefits",
    ],
    "cup": [
        "Steel cup - 50 to 150 rupees reusable forever",
        "Clay kulhad - 5 to 10 rupees biodegradable traditional Indian cup",
    ],
    "plate": [
        "Steel plate - 80 to 200 rupees reusable for decades",
        "Banana leaf plate - 2 to 5 rupees 100 percent biodegradable",
        "Areca palm leaf plate - 5 to 10 rupees natural and compostable",
    ],
}


def search_eco_products(query):
    query_lower = query.lower()
    for category, alternatives in PRODUCTS.items():
        if any(word in query_lower for word in category.split()):
            result = f"Eco alternatives to {category}:\n"
            result += "\n".join(f"- {a}" for a in alternatives)
            return result
    return (
        f"For eco alternatives to {query} check these Indian stores:\n"
        "- EcoKart.in India's eco marketplace\n"
        "- Bare Necessities barenecessities.in zero waste store\n"
        "- Brown Living brownliving.in sustainable products\n"
        "- Local Fabindia or Khadi Gramudyog store"
    )