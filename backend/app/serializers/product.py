from app.models.product import Product


def serialize_product(product: Product) -> dict:
    return {
        "id": product.id,
        "barcode": product.barcode,
        "name": product.name,
        "brand": product.brand,
        "category": product.category,
        "eco_score": product.eco_score,
        "nutriscore": product.nutriscore,
        "average_price": product.average_price,
    }