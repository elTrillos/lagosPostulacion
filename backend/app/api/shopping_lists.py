from flask import Blueprint, request, jsonify
from app import db
from app.api import api
from app.models import Product, ShoppingList, ListItem
from app.serializers.shopping_list import serialize_list
from app.services.openfoodfacts import fetch_product_by_barcode
from app.services.openpriceengine import fetch_openprice_product
from datetime import datetime, timedelta

@api.route("lists", methods=["POST"])
def create_list():
    data = request.json or {}

    name = data.get("name")
    budget = data.get("budget")
    user_id = data.get("user_id")

    if not all([name, budget, user_id]):
        return {"error": "name, budget and user_id required"}, 400

    shopping_list = ShoppingList(
        name=name,
        budget=float(budget),
        user_id=user_id,
    )

    db.session.add(shopping_list)
    db.session.commit()

    return serialize_list(shopping_list), 201

@api.route("lists/<int:list_id>", methods=["DELETE"])
def delete_list(list_id):
    shopping_list = ShoppingList.query.get_or_404(list_id)

    db.session.delete(shopping_list)
    db.session.commit()

    return {"status": "deleted"}

@api.route("lists/<int:list_id>/items", methods=["POST"])
def add_item_to_list(list_id):
    shopping_list = ShoppingList.query.get_or_404(list_id)

    data = request.json or {}
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))
    price = data.get("price")

    if not all([product_id, price]):
        return {"error": "product_id and price required"}, 400

    item = ListItem.query.filter_by(
        shopping_list_id=list_id,
        product_id=product_id,
    ).first()

    if item:
        item.quantity += quantity
        item.price = float(price)
    else:
        item = ListItem(
            shopping_list_id=list_id,
            product_id=product_id,
            quantity=quantity,
            price=float(price),
        )
        db.session.add(item)

    db.session.commit()

    return serialize_list(shopping_list)

@api.route("lists/<int:list_id>/items/<int:product_id>", methods=["DELETE"])
def remove_item_from_list(list_id, product_id):
    item = ListItem.query.filter_by(
        shopping_list_id=list_id,
        product_id=product_id,
    ).first_or_404()

    db.session.delete(item)
    db.session.commit()

    return {"status": "removed"}


@api.route("lists/<int:list_id>/scan/<barcode>", methods=["POST"])
def scan_and_add_product(list_id, barcode):
    shopping_list = ShoppingList.query.get_or_404(list_id)
    data = request.json or {}

    price = data.get("price")
    if price is None:
        return {"error": "price required"}, 400

    product = Product.query.filter_by(barcode=barcode).first()

    if not product:
        product_data = fetch_product_by_barcode(barcode)
        if not product_data:
            return {"error": "Product not found"}, 404

        product = Product(**product_data)
        db.session.add(product)
        db.session.flush()

    item = ListItem.query.filter_by(
        shopping_list_id=list_id,
        product_id=product.id,
    ).first()

    if item:
        item.quantity += 1
        item.price = float(price)
    else:
        item = ListItem(
            shopping_list_id=list_id,
            product_id=product.id,
            quantity=1,
            price=float(price),
        )
        db.session.add(item)

    db.session.commit()

    return serialize_list(shopping_list)

@api.route("lists/<int:list_id>/scan/openprice/<query>", methods=["POST"])
def scan_and_add_openprice(list_id, query):
    shopping_list = ShoppingList.query.get_or_404(list_id)
    data = request.json or {}

    # fallback price if not provided by API
    fallback_price = data.get("price")

    product_data = fetch_openprice_product(query)
    if not product_data:
        if fallback_price is None:
            return {"error": "Product not found and no price provided"}, 404
        product_data = {
            "name": query,
            "price": fallback_price,
            "barcode": "",
            "brand": "",
            "category": "",
        }

    # check if product exists in DB
    product = Product.query.filter_by(barcode=product_data.get("barcode")).first()
    if not product:
        product = Product(
            name=product_data["name"],
            average_price=product_data["price"],
            brand=product_data.get("brand"),
            category=product_data.get("category"),
            barcode=product_data.get("barcode") or None
        )
        db.session.add(product)
        db.session.flush()

    # add to list
    item = ListItem.query.filter_by(
        shopping_list_id=list_id,
        product_id=product.id
    ).first()

    if item:
        item.quantity += 1
        item.price = product_data["price"]
    else:
        item = ListItem(
            shopping_list_id=list_id,
            product_id=product.id,
            quantity=1,
            price=product_data["price"]
        )
        db.session.add(item)

    db.session.commit()
    return serialize_list(shopping_list)


@api.route("/lists/<int:list_id>", methods=["GET"])
def get_list_details(list_id):
    shopping_list = ShoppingList.query.get_or_404(list_id)
    return serialize_list(shopping_list)
