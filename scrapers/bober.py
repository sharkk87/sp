from module import timer, Scraper, write_csv_in_file

URL = 'http://magazinbober.ru/catalog/'
CITY = '?geo=312186'
COUNT = '&count=100&'


def check_group(soup):
    if soup.find('div', class_='main').find('ul', class_='subrubrics'):
        return True
    else:
        return False


def make_url(url):
    return 'http://magazinbober.ru' + url.find('a').get('href') + CITY + COUNT


@timer
def main():
    # Get main links
    soup = Scraper.get_soup(URL)
    main_links_soup = soup.find('ul', class_='list-rubrics').find_all('li')
    main_links = [make_url(link) for link in main_links_soup]

    # Fill dict to links
    all_links = {}
    for link in main_links:
        soup = Scraper.get_soup(link)
        if check_group(soup):
            sub_links = soup.find('ul', class_='subrubrics').find_all('li')
            [main_links.append(make_url(url)) for url in sub_links]
        else:
            try:
                all_links[link] = int(soup.find('ul', class_='pager').find_all('li')[-2].text)
            except AttributeError:
                all_links[link] = 1
            # print(link, all_links[link])

    # Go in all pages with scrap data into list
    data_list = []
    title = 'Бобёр'
    for page, total_page in all_links.items():
        for page_num in range(1, total_page + 1):
            page_data = page + 'PAGEN_1=' + str(page_num)
            soup = Scraper.get_soup(page_data)

            try:
                data = soup.find('ul', class_='list-products').find_all('li')
            except AttributeError:
                print('No data this page: {}'.format(page_data))
                continue

            for i in data:
                name = i.find('span', class_='ttl').text.split()
                name = ' '.join(name)

                url = i.find('a', class_='body').get('href')
                url = 'http://magazinbober.ru' + url + CITY

                try:
                    url_image = i.find('span', class_='img-wrap').find('img').get('src')
                    url_image = 'http://magazinbober.ru' + url_image
                except AttributeError:
                    url_image = ''

                if i.find('span', class_='price'):
                    price = i.find('span', class_='price').text.strip()
                    available = 'В наличии'

                    if i.find('div', class_='price-wrap'):
                        available = 'Нет в наличии'

                else:
                    price = ''
                    available = 'Нет в наличии'

                data = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url, 'url_image': url_image}
                data_list.append(data)

    # Create csv-file and write data
    write_csv_in_file(data_list)
    print('Собрано данных: {}'.format(len(data_list)))


if __name__ == '__main__':
    main()
