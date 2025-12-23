import os
import requests
from datetime import datetime

OPEN_PRICE_ENGINE_URL = "https://api.openpricengine.com/v1/products"
OPEN_PRICE_ENGINE_API_KEY = os.getenv("OPEN_PRICE_ENGINE_API_KEY")


def fetch_openprice_product(query: str, limit=1):
    headers = {
        "Authorization": f"Bearer {OPEN_PRICE_ENGINE_API_KEY}",
        "Accept": "application/json",
    }
    params = {
        "query": query,
        "limit": limit
    }

    response = requests.get(OPEN_PRICE_ENGINE_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    if not data.get("products"):
        return None

    product = data["products"][0]  # take first result
    return {
        "name": product.get("name"),
        "price": product.get("price", {}).get("amount"),
        "unit": product.get("price", {}).get("unit"),
        "barcode": product.get("barcode") or "",
        "brand": product.get("brand") or "",
        "category": product.get("category") or "",
        "url": product.get("url") or "",
    }
