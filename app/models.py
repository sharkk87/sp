from app import db


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop = db.Column(db.String(20))
    title = db.Column(db.String(300))
    price = db.Column(db.Float(precision='10, 2'))
    available = db.Column(db.String(20))
    url = db.Column(db.String(400))
    url_image = db.Column(db.String(250))
