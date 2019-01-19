from django.shortcuts import render
import pymysql


def post_list(request):

    return render(request, 'page/index.html')


def get_query(s):
    l = s.split()

    search = {}
    if 'or' in s:
        for i in range(len(l)):
            if l[i] == 'or' or l[i] in search.values():
                continue
            elif i == len(l) - 1:
                search[l[i]] = None
                break
            elif l[i + 1] != 'or':
                search[l[i]] = None
            else:
                search[l[i]] = l[i + 2]
    else:
        for i in l:
            search[i] = None

    s_l = "name LIKE '%"

    s_or = ' OR '
    s_and = ' AND '

    itog = 'SELECT * from main WHERE '
    for i, v in search.items():
        if v == None:
            itog += "(" + s_l + i + r"%'" + ")" + s_and
        elif v != None:
            itog += "(" + s_l + i + r"%'" + s_or + s_l + v + r"%'" + ")" + s_and

    if itog[-1] == ')':
        return itog + 'LIMIT 500;'
    else:
        return itog[:-5] + 'LIMIT 500;'


def get_name(request):
    q = request.GET['q']

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='0000',
                                 db='my_parser',
                                 charset="utf8")

    cur = connection.cursor()
    sql = get_query(q)
    cur.execute(sql)

    # data['title'], data['name'], data['price'], data['available'], data['url']

    data = [row for row in cur.fetchall()]

    return render(request, 'page/search.html', {'data': data, 'query': q})


