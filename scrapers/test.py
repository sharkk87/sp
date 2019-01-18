from bs4 import BeautifulSoup

import requests

url = 'http://www.kontinent.ru/catalog/lkm/?price_min=&price_max=&photo=N&sort=price_up&countonpage=120'

html = requests.get(url)
soup = BeautifulSoup(html.text, 'lxml')

try:
    data = soup.find('div', class_='products_block').find_all('div', class_='cart')
except AttributeError:
    print('No')

for i in data:
    print(i.find('div').find('a').text.split())
