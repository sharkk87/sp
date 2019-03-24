from module import Scraper, timer, write_csv_in_file


URL = 'https://cov35.ru/katalog/'

data_list = []


def get_data(soup):
    global data_list
    title = 'Центр отопления и вентиляции'

    data = soup.find_all('div', recursive=False)
    for i in data:
        name = i.find('div', class_='main-catalog-item-title').text.split()
        name = ' '.join(name)

        url = i.find('div', class_='catalog-item-image').find('a').get('href')

        url_image = i.find('div', class_='catalog-item-image').find('img').get('src')
        url_image = 'https://cov35.ru' + url_image

        try:
            price = i.find('div', class_='main-catalog__price').find('span', class_='price-old').next_sibling.strip()
        except AttributeError:
            price = i.find('div', class_='main-catalog__price').text.strip()

        if price == 'По запросу':
            available = 'Под заказ'
        else:
            available = 'В наличии'

        data = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url, 'url_image': url_image}
        data_list.append(data)


@timer
def main():
    links = []
    soup = Scraper.get_soup(URL)
    soup_links = soup.find_all('div', class_='catalog-categody-title-outer')
    for i in soup_links:
        links.append(i.find('a').get('href'))

    for i in links:
        soup = Scraper.get_soup(i)
        data_catalog = soup.find('div', class_='catalogWrap')

        if data_catalog:
            get_data(data_catalog)
        else:
            soup_links = soup.find_all('div', class_='catalog-categody-title-outer')
            for j in soup_links:
                links.append(j.find('a').get('href'))

    write_csv_in_file(data_list)
    print('Собрано данных: {}'.format(len(data_list)))


if __name__ == '__main__':
    main()
