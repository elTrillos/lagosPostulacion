import requests
from datetime import datetime

OPENFOODFACTS_URL = "https://world.openfoodfacts.org/api/v2/product/{}.json"
OFF_SEARCH_URL = "https://world.openfoodfacts.org/api/v2/search"

def fetch_product_by_barcode(barcode: str) -> dict | None:
    resp = requests.get(OPENFOODFACTS_URL.format(barcode), timeout=5)

    if resp.status_code != 200:
        return None

    data = resp.json()

    if data.get("status") != 1:
        return None

    product = data["product"]

    return {
        "barcode": barcode,
        "name": product.get("product_name", "").strip(),
        "brand": product.get("brands", "").split(",")[0].strip(),
        "category": product.get("categories", "").split(",")[0].strip(),
        "eco_score": parse_eco_score(product),
        "nutriscore": product.get("nutriscore_grade", "").upper()[:1],
        "average_price": None,
        "last_fetched_at": datetime.utcnow(),
    }


def parse_eco_score(product: dict) -> float | None:
    score = product.get("ecoscore_score")
    try:
        return float(score) if score is not None else None
    except ValueError:
        return None
    

def search_openfoodfacts(query: str, country="chile", limit=20):
    params = {
        "countries": country,
        "categories": "food",
        "search_terms": query,
        "page_size": limit
    }
    resp = requests.get(OFF_SEARCH_URL, params=params, timeout=5)
    resp.raise_for_status()
    data = resp.json()

    results = []
    for item in data.get("products", []):
        eco_score = item.get("ecoscore_score")
        if eco_score is None:
            continue  # ignore null eco-scores

        results.append({
            "name": item.get("product_name"),
            "barcode": item.get("code"),
            "brand": item.get("brands"),
            "category": item.get("categories"),
            "eco_score": eco_score,
            "nutriscore": item.get("nutriscore_grade"),
        })
    # Sort descending by eco_score
    results.sort(key=lambda x: x["eco_score"], reverse=True)
    return results
