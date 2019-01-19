from app import app
from app import models
from flask import render_template, request


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/catalog/')
def catalog():
    q = request.args.get('q')

    if q:
        user_query = q
    else:
        user_query = 'Пустой запрос'

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    data = models.Products.query

    data_total = len(data.all())

    pages = data.paginate(page=page, per_page=64)

    return render_template('catalog.html', data=data, pages=pages, data_total=data_total, user_query=user_query)
