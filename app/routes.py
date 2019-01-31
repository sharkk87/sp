from app import app
from app import models
from flask import render_template, request
from sqlalchemy import and_, or_


def get_query(s):
    s = ' '.join(s.split()).lower()
    s = s.split(' ')

    result = []
    list_index = 0
    check_bracket = False
    for i in s:
        if i.startswith('('):
            check_bracket = True
            # print(list_index, i, check_bracket)
            result.append([])

        elif i.endswith(')'):
            # print(list_index, i, check_bracket)
            check_bracket = False

        if check_bracket and i.startswith('('):
            # print(list_index, i, check_bracket)
            result[list_index].append(i[1:])

        elif check_bracket:
            # print(list_index, i, check_bracket)
            result[list_index].append(i)

        elif i.endswith(')'):
            # print(list_index, i, check_bracket)
            result[list_index].append(i[:-1])

            list_index += 1

        else:
            # print(list_index, i, check_bracket)
            result.append(i)

            list_index += 1

    return result


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/catalog/')
def catalog():
    q = request.args.get('q')
    q = ' '.join(q.split()).lower()

    if q == ' ':
        user_query = get_query('Вы ничего не запросили!')
        user_query_output = 'Вы ничего не запросили!'
    elif q:
        user_query = get_query(q)
        user_query_output = q
    else:
        user_query = get_query('Вы ничего не запросили!')
        user_query_output = 'Вы ничего не запросили!'

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    count_or = [i for i, v in enumerate(user_query) if isinstance(v, list)]
    if len(count_or) == 1:
        data = models.Products.query.filter(
            or_(
                models.Products.title.contains(i) for i in user_query[count_or[0]]
            ),
            and_(
                models.Products.title.contains(i) for i in user_query if isinstance(i, str)
            )
        ).order_by(models.Products.price)
    elif len(count_or) == 2:
        data = models.Products.query.filter(
            or_(
                models.Products.title.contains(i) for i in user_query[count_or[0]]
            ),
            or_(
                models.Products.title.contains(i) for i in user_query[count_or[1]]
            ),
            and_(
                models.Products.title.contains(i) for i in user_query if isinstance(i, str)
            )
        ).order_by(models.Products.price)
    elif len(count_or) == 3:
        data = models.Products.query.filter(
            or_(
                models.Products.title.contains(i) for i in user_query[count_or[0]]
            ),
            or_(
                models.Products.title.contains(i) for i in user_query[count_or[1]]
            ),
            or_(
                models.Products.title.contains(i) for i in user_query[count_or[2]]
            ),
            and_(
                models.Products.title.contains(i) for i in user_query if isinstance(i, str)
            )
        ).order_by(models.Products.price)
    else:
        data = models.Products.query.filter(
            and_(
                models.Products.title.contains(i) for i in user_query if isinstance(i, str)
            )
        ).order_by(models.Products.price)

    data_total = len(data.all())

    pages = data.paginate(page=page, per_page=64)

    return render_template('catalog.html', data=data, pages=pages, data_total=data_total, user_query=user_query, user_query_output=user_query_output)
