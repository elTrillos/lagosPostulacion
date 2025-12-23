from app import db

class ShoppingList(db.Model):
    __tablename__ = "shopping_lists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="shopping_lists")

    items = db.relationship(
        "ListItem",
        back_populates="shopping_list",
        cascade="all, delete-orphan"
    )

    def total_cost(self):
        return sum(item.price * item.quantity for item in self.items)

    def __repr__(self):
        return f"<ShoppingList {self.name}>"
