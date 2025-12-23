from app.models.list_item import ListItem
from app.models.shopping_list import ShoppingList
from app.serializers.product import serialize_product


def serialize_list_item(item: ListItem):
    return {
        "id": item.id,
        "quantity": item.quantity,
        "price": item.price,
        "subtotal": item.price * item.quantity,
        "product": serialize_product(item.product),
    }


def serialize_list(shopping_list: ShoppingList):
    return {
        "id": shopping_list.id,
        "name": shopping_list.name,
        "budget": shopping_list.budget,
        "total_cost": shopping_list.total_cost(),
        "items": [serialize_list_item(i) for i in shopping_list.items],
    }