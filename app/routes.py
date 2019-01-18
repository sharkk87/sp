from app import app
from app import models
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalog')
def catalog():
    data = models.Products.query.all()

    return render_template('catalog.html', data=data)