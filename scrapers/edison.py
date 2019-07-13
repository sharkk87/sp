import requests
from module import timer, Scraper, write_csv_in_file
from bs4 import BeautifulSoup


URL = 'https://www.edisonlight.ru'
COOKIES = {
    'BITRIX_SM_IP_CITY_NAME':'%D0%92%D0%BE%D0%BB%D0%BE%D0%B3%D0%B4%D0%B0',
    'BITRIX_SM_IP_CITY_LOCATION_ID_NEW':'5846',
}
COUNT = '?count=80'
PAGE = '&PAGEN_1='


def get_pagination(soup):
    try:
        total_pages = soup.find('div', class_='pagination').find_all('li', class_='pagination__item')[-2]\
                                                           .find('a').get('title')
    except AttributeError:
        total_pages = 1
    return int(total_pages)


def get_data(soup, title='Эдисон'):
    soup_items = soup.find('div', class_='catalog_items').find_all('div', class_='catalog_item')

    data_items = []
    for item in soup_items:
        name = item.find('div', class_='item_desc').find('span').text.split()
        name = ' '.join(name)

        url = URL + item.find('div', class_='item_desc').find('a').get('href')

        url_image = item.find('div', class_='item_img').find('img').get('src')
        url_image = URL + url_image

        try:
            price = item.find('div', class_='item_buy').find('span', class_='new').get_text(' ')
        except AttributeError:
            price = ''

        available = item.find('div', class_='presence').find('span').text
        if available == 'Доступно к заказу':
            available = 'Под заказ'

        data_item = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url, 'url_image': url_image}
        data_items.append(data_item)

    return data_items


@timer
def main():
    with requests.session() as s:
        s.cookies.update(COOKIES)

        soup = BeautifulSoup(s.get(URL+'/catalog').text, 'lxml')
        print(soup.find('div', class_='city_list').find('a').text)

        main_list = (URL + i.find('a').get('href') + COUNT for i in soup.find('ul', class_='listCatalog__list')\
                                                                 .find_all('li', class_='listCatalog__item', recursive=False))

        data_list = []
        for i in main_list:
            soup = BeautifulSoup(s.get(i).text, 'lxml')
            pages = get_pagination(soup)

            for link in range(1, pages+1):
                url = i+PAGE+str(link)
                data_list += get_data(BeautifulSoup(s.get(url).text, 'lxml'))

    write_csv_in_file(data_list)
    print('Собрано данных: {}'.format(len(data_list)))

if __name__ == '__main__':
    main()
