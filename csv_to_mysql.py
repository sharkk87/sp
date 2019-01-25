import csv
import os


basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

from app import db
from app.models import Products


# with open('/home/iliya/PycharmProjects/stroy-parser35/scrapers/shop_csv/25012019_upravdom.csv') as file:
#     reader = csv.reader(file)
#     data = [i for i in reader]
#
# for i in data:
#     db.session.add(Products(shop=i[0], title=i[1], price=i[2], available=i[3], url=i[4]))
#
# db.session.commit()
