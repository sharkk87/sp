import csv, os, glob
import sys
sys.path.append('../')

from datetime import datetime
from app import db
from app.models import Products


basedir = os.path.abspath(os.path.dirname(__file__))

shop = ['apline',
        'bober',
        'centrsm',
        'kontinent',
        'lider',
        'sanvol',
        'tdsot',
        'upravdom',
        # 'evrostroy',
        'akson',
        'idd',
        'cov',
        ]


def get_last_files():
    all_files = glob.glob(basedir + '/shop_csv/*.csv')

    shop_dic = {}
    for i in shop:
        shop_dic[i] = []

    for file in all_files:
        date_file = file.split('/')[-1][:8]
        date_file = datetime.strptime(date_file, '%d%m%Y')

        name_file = file.split('_')[-1]
        name_file = name_file.split('.')[0]

        if name_file.startswith('apline'):
            shop_dic[name_file].append((date_file, file))
        elif name_file.startswith('bober'):
            shop_dic[name_file].append((date_file, file))
        elif name_file.startswith('centrsm'):
            shop_dic[name_file].append((date_file, file))
        elif name_file.startswith('kontinent'):
            shop_dic[name_file].append((date_file, file))
        elif name_file.startswith('lider'):
            shop_dic[name_file].append((date_file, file))
        elif name_file.startswith('sanvol'):
            shop_dic[name_file].append((date_file, file))
        elif name_file.startswith('tdsot'):
            shop_dic[name_file].append((date_file, file))
        elif name_file.startswith('upravdom'):
            shop_dic[name_file].append((date_file, file))
        # elif name_file.startswith('evrostroy'):
        #     shop_dic[name_file].append((date_file, file))
        elif name_file.startswith('akson'):
            shop_dic[name_file].append((date_file, file))
        elif name_file.startswith('idd'):
            shop_dic[name_file].append((date_file, file))
        elif name_file.startswith('cov'):
            shop_dic[name_file].append((date_file, file))

    last_list = []
    for i, v in shop_dic.items():
        last_list.append(sorted(v, reverse=True)[0][1])

    return last_list


def fix_price(s):
    s = s.replace(',', '.')
    s = s.split()

    price = []
    for i in s:
        try:
            float(i)
            price.append(i)
        except ValueError:
            pass

    if price:
        price = ''.join(price)
    else:
        price = '0'

    return price


files = get_last_files()
total = 0

db.engine.execute('TRUNCATE products;')

print('Отчет на: {}'.format(datetime.now()))
for path in files:
    with open(path) as f:
        reader = csv.reader(f)
        data = [i for i in reader]
        total += len(data)

        for i in data:
            db.session.add(Products(shop=i[0], title=i[1], price=fix_price(i[2]), available=i[3], url=i[4], url_image=i[5]))

        print('С файла {} загружено {} данных'.format(path.split('/')[-1], len(data)))
        db.session.commit()

print('ИТОГО: {}'.format(total))
print('#'*50)

db.session.commit()
db.session.close()
