from app import app
from app import models
from flask import render_template, request
from sqlalchemy import and_, or_


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/catalog/')
def catalog():
    s = ['плит', 'клей', ['кнауф', 'knauf', 'knuf'], ['20', '25'], 'кг']

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

    # data = models.Products.query.filter\
    #     (
    #         and_(models.Products.title.contains(i) for i in s if isinstance(i, str)),
    #         or_(models.Products.title.contains(j) for i in s if isinstance(i, list) for j in i)
    #     )

    data = models.Products.query.filter\
        (
            and_(
                models.Products.title.contains(s[0]),
                models.Products.title.contains(s[1]),
                or_(
                    models.Products.title.contains(s[2][0]),
                    models.Products.title.contains(s[2][1]),
                    models.Products.title.contains(s[2][2])
                ),
                or_(
                    models.Products.title.contains(s[3][0]),
                    models.Products.title.contains(s[3][1])
                )
            )
        )

    data_total = len(data.all())

    pages = data.paginate(page=page, per_page=64)

    return render_template('catalog.html', data=data, pages=pages, data_total=data_total, user_query=user_query)
