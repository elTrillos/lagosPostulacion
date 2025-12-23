from flask import Blueprint, request
from app import db
from app.api import api
from app.models import Product, ShoppingList, ListItem
from datetime import datetime, timedelta
from app.services.openfoodfacts import fetch_product_by_barcode
from app.serializers.product import serialize_product

PRODUCT_TTL = timedelta(hours=12)

@api.route("products/barcode/<barcode>", methods=["GET"])
def get_product_by_barcode(barcode):
    product = Product.query.filter_by(barcode=barcode).first()

    if product:
        is_fresh = datetime.utcnow() - product.last_fetched_at < PRODUCT_TTL
        if is_fresh:
            return serialize_product(product)

    data = fetch_product_by_barcode(barcode)
    if not data:
        return {"error": "Product not found"}, 404

    if product:
        for key, value in data.items():
            setattr(product, key, value)
    else:
        product = Product(**data)
        db.session.add(product)
    db.session.commit()

    return serialize_product(product)

@api.route("products/search")
def search_products():
    q = request.args.get("q", "")

    products = Product.query.filter(
        Product.name.ilike(f"%{q}%")
    ).limit(20).all()

    return [serialize_product(p) for p in products]

