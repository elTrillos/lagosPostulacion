import requests

BASE_URL = "https://world.openfoodfacts.org/api/v0/product"

def fetch_product_by_barcode(barcode: str) -> dict | None:
    url = f"{BASE_URL}/{barcode}.json"
    r = requests.get(url, timeout=10).json()

    if r.get("status") != 1:
        return None

    p = r["product"]

    return {
        "barcode": barcode,
        "name": p.get("product_name"),
        "brand": p.get("brands"),
        "category": (p.get("categories") or "").split(",")[0],
        "eco_score": p.get("ecoscore_score"),
        "nutriscore": p.get("nutriscore_grade"),
    }
