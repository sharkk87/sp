import requests
from bs4 import BeautifulSoup

from module import timer, Scraper, write_csv_in_file


URL = 'http://eltsnab.ru/catalogue'
URL_SHORT = 'http://eltsnab.ru'


# Get list with urls contains data
def get_urls(url):
    soup = Scraper.get_soup(url)

    links = [URL_SHORT + i.get('href')[2:] for i in soup.find('div', class_='main').find_all('a', class_='table-button')]
    return links


def get_data(url, title='Электротехснаб'):
    soup_items = Scraper.get_soup(url).find('div', class_='main').find_all('article', class_='item')

    data_items = []
    for item in soup_items:
        name = item.find('div', class_='heading').find('a').text.split()
        name = ' '.join(name)

        url = item.find('div', class_='heading').find('a').get('href')
        url = URL_SHORT + url.replace('..', '')

        url_image = item.find('div', class_='figure').find('img').get('src')

        price = item.find('div', class_='price').find('div', class_='new').text.strip()

        if price:
            available = 'В наличии'
        else:
            available = 'Под заказ'

        data_item = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url, 'url_image': url_image}
        data_items.append(data_item)

    return data_items

@timer
def main():
    links = [i for i in get_urls(URL)]

    data_list = []
    for i in links:
        urls = get_urls(i)
        if urls:
            links += urls
        else:
            data_list += get_data(i)

    write_csv_in_file(data_list)
    print('Собрано данных: {}'.format(len(data_list)))


if __name__ == '__main__':
    main()
