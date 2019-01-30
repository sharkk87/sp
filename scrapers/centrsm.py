from module import Scraper, timer, write_csv_in_file

URL = 'https://dom35.ru/'


@timer
def main():
    # Get main links
    soup = Scraper().get_soup(URL)
    main_links_data = soup.find('div', class_='categories_grid').find_all('div', class_='item')

    main_links = (URL[:-1] + i.find('a').get('href') for i in main_links_data)

    # Fill dict to links with integer paginator
    links = {}
    for link in main_links:
        soup = Scraper.get_soup(link)
        page = int(soup.find('div', id='product-list').find('ul', class_='pagination').find_all('li')[-2].text)
        links[link] = page

    # Fill list to data
    data_list = []
    title = 'Центр СМ'
    for page, total_page in links.items():
        for page_num in range(1, total_page + 1):
            page_data = page + '?page=' + str(page_num)
            soup = Scraper.get_soup(page_data)
            try:
                data = soup.find('div', class_='product-list').find_all('div', class_='product')
            except:
                print('No data this page: {}'.format(page_data))
                continue

            for i in data:
                name = i.find('a').get('title').split()
                name = ' '.join(name)

                url = 'https://dom35.ru' + i.find('a').get('href').strip()

                url_image = i.find('div', class_='image_wrap').find('img').get('src')
                url_image = 'https://dom35.ru' + url_image

                price = i.find('meta', itemprop='price').get('content')

                available = i.find('div', class_='stock').text.strip()

                data = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url, 'url_image': url_image}
                data_list.append(data)

    # Create csv-file and write data
    write_csv_in_file(data_list)
    print('Собрано данных: {}'.format(len(data_list)))


if __name__ == '__main__':
    main()
