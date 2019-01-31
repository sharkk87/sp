from module import Scraper, timer, write_csv_in_file

URL = 'http://www.kontinent.ru'
SHOW_120 = '?price_min=&price_max=&photo=N&sort=price_up&countonpage=120'


@timer
def main():
    # Get main links
    soup = Scraper.get_soup(URL)
    main_links_data = soup.find('ul', class_='catalog_menu').find_all('li', class_='has_children')
    main_links = (URL + link.find('a').get('href') + SHOW_120 for link in main_links_data)

    # Fill dict links with int pagination
    links = {}
    for link in main_links:
        soup = Scraper.get_soup(link)
        page = int(soup.find('div', class_='pagination').find_all('li')[-1].text)
        links[link] = page

    # Go all links and fill list to data
    data_list = []
    title = 'Континент'
    for page, total_page in links.items():
        for page_num in range(1, total_page + 1):
            url = page + '&page=' + str(page_num)
            soup = Scraper.get_soup(url)

            try:
                data = soup.find('div', class_='products_block').find_all('div', class_='cart')
            except AttributeError:
                print('No data this page: {}'.format(url))
                continue

            for i in data:
                name = i.find('div').find('a').text.split()
                name = ' '.join(name)

                url = URL + i.find('div').find('a').get('href').strip()

                try:
                    url_image = i.find('a', class_='for_img').find('img').get('src')
                    url_image = URL + url_image
                except AttributeError:
                    url_image = ''

                try:
                    price = i.find('span', class_='price_one').text.strip()
                except AttributeError:
                    price = i.find('span', class_='price_new').text.strip()

                if i.find('button', class_='buy_button'):
                    available = 'В наличии'
                else:
                    available = 'Под заказ'

                data = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url, 'url_image': url_image}
                data_list.append(data)

    # Create csv-file and write data
    write_csv_in_file(data_list)
    print('Собрано данных: {}'.format(len(data_list)))


if __name__ == '__main__':
    main()
