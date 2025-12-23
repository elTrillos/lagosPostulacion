from app import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(32), unique=True, index=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))

    category = db.Column(db.String(100))

    eco_score = db.Column(db.Float)
    nutriscore = db.Column(db.String(1))

    average_price = db.Column(db.Float)

    def __repr__(self):
        return f"<Product {self.name}>"
