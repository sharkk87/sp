from module import Scraper, timer, write_csv_in_file


URL = 'http://www.tdsot.ru/catalog/'
COUNT_100 = '?count=100'
PAGE = '&PAGEN_1='


@timer
def main():
    soup = Scraper.get_soup(URL)
    main_links_data = soup.find('div', class_='catalog').find_all('tr')
    main_links = (URL[:19] + link.find('a').get('href') + COUNT_100 for link in main_links_data)

    all_links = {}
    for link in main_links:
        soup = Scraper.get_soup(link)
        try:
            total_pages = int(soup.find('ul', class_='pagination').find_all('li')[-1].find('a').get('href').split('=')[-1])
        except AttributeError:
            total_pages = 1

        all_links[link] = total_pages
        # print(link, total_pages)

    data_list = []
    title = 'стройОПТторг'
    available = 'В наличии'
    for page, total_page in all_links.items():
        for page_num in range(1, total_page + 1):
            soup = Scraper.get_soup(page + PAGE + str(page_num))
            data = soup.find('table', class_='catalog-table').find_all('tr')

            for i in data:
                name = i.find('td', class_='name').find('a').text.split()
                name = ' '.join(name)

                url = URL[:19] + i.find('td', class_='name').find('a').get('href')

                url_image = i.find('td', class_='pic').find('img').get('src')
                url_image = 'http://www.tdsot.ru' + url_image

                price = i.find('td', class_='price').find('b').text

                data = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url, 'url_image': url_image}
                data_list.append(data)

    # Create csv-file and write data
    write_csv_in_file(data_list)
    print('Собрано данных: {}'.format(len(data_list)))


if __name__ == '__main__':
    main()
