from app import db


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop = db.Column(db.String(20))
    title = db.Column(db.String(300))
    price = db.Column(db.String(20))
    available = db.Column(db.String(20))
    url = db.Column(db.String(400))
