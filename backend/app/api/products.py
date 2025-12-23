from flask import Blueprint, request
from app import db
from app.api import api
from app.models import Product
from app.services.openfoodfacts import fetch_product_by_barcode

@api.route("products/barcode/<barcode>", methods=["GET"])
def get_product_by_barcode(barcode):
    product = Product.query.filter_by(barcode=barcode).first()

    if product:
        return serialize_product(product)

    data = fetch_product_by_barcode(barcode)
    if not data:
        return {"error": "Product not found"}, 404

    product = Product(**data)
    db.session.add(product)
    db.session.commit()

    return serialize_product(product)

@api.route("products/search")
def search_products():
    q = request.args.get("q", "")

    products = Product.query.filter(
        Product.name.ilike(f"%{q}%")
    ).limit(20)

    return [serialize_product(p) for p in products]


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
