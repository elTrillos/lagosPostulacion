from app import db

class ListItem(db.Model):
    __tablename__ = "list_items"

    id = db.Column(db.Integer, primary_key=True)

    shopping_list_id = db.Column(
        db.Integer,
        db.ForeignKey("shopping_lists.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)

    shopping_list = db.relationship("ShoppingList", back_populates="items")
    product = db.relationship("Product")

    def __repr__(self):
        return f"<ListItem {self.product.name} x{self.quantity}>"
