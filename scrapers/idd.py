from module import Scraper, timer, write_csv_in_file

URL = 'https://idd35.ru/'
PAGE = '?page='


@timer
def main():
    soup = Scraper.get_soup(URL)
    main_links_soup = soup.find('ul', class_='dropdown-menu dropdown-menu_theme_am').find_all('li', class_='dropdown-submenu')

    main_links = [URL[:-1] + i.find('a').get('href') for i in main_links_soup]

    data_list = []
    for i in main_links:
        soup = Scraper.get_soup(i)
        pages = int(soup.find('ul', class_='pagination').find_all('li')[-2].text)
        # print(i, pages)

        for j in range(1, pages+1):
            url = i + PAGE + str(j)
            # print(url)

            soup = Scraper.get_soup(url)
            data_soup = soup.find('ul', class_='products').find_all('li', class_='products__item')

            title = 'Идеи для дома'
            for item in data_soup:
                name = item.find('div', class_='products__text').text.split()
                name = ' '.join(name)

                url = item.find('div', class_='products__name').find('a').get('href')
                url = URL[:-1] + url

                url_image = item.find('div', class_='products__image').find('div', class_='image').find('img').get('src')
                url_image = URL[:-1] + url_image

                price = item.find('span', class_='products__price').text.strip()

                available = item.find('span', class_='stocks__msg').text.strip()
                if available != 'Под заказ':
                    available = 'В наличии'

                data = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url, 'url_image': url_image}
                data_list.append(data)

    write_csv_in_file(data_list)
    print('Собрано данных: {}'.format(len(data_list)))


if __name__ == '__main__':
    main()
