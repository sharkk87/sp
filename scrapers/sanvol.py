from module import Scraper, timer, write_csv_in_file

URL = 'http://sanvol.ru/'


def get_pagination(soup):
    data = soup.find('section', attrs={'class': 'content'}).find('p', attrs={'class': None}).find_all('a', class_='page_link')
    if data:
        page_str = data[-1].text.strip()

        if page_str == '>':
            # /shop/polypropylene/polypropylene-white-aqua-pro/page-9/ -> 9
            page = int(data[-1].get('href').split('-')[-1][:-1])
        else:
            page = int(page_str)
    else:
        page = 1
    return page


def get_data(soup, title='Сантехника', available='В наличии'):
    data = soup.find('section', class_='content').find_all('div', class_='list')
    data_items = []

    for item in data:
        try:
            name = item.find('a', class_='next').text.split()
            name = ' '.join(name)
        except AttributeError:
            continue

        url = URL[:-1] + item.find('a', class_='next').get('href')

        price = item.find('div', class_='price').text

        data_item = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url}
        data_items.append(data_item)
    return data_items


@timer
def main():
    soup = Scraper.get_soup(URL)
    main_links_data = soup.find('ul', class_='shop_list').find_all('li', attrs={'class': None})
    main_links_data_sub = soup.find('ul', class_='shop_list').find_all('li', attrs={'class': 'sub'})

    main_links = [URL[:-1] + link.find('a').get('href') for link in main_links_data]
    main_links_sub = [URL[:-1] + link.find('a').get('href') for link in main_links_data_sub]

    for link in main_links_sub:
        soup = Scraper.get_soup(link)
        data = soup.find('ul', class_='shop_list').find('li', class_='selected').find_all('ul', class_='dop')[-1]
        data = data.find_all('li')

        # data = data_dop.find_all('li', attrs={'class': None})
        # data_sub = data_dop.find_all('li', attrs={'class': 'sub'})

        for i in data:
            if i.get('class') is None:
                # print(i.find('a').get('href'), i.get('class'))
                main_links.append(URL[:-1] + i.find('a').get('href'))
            else:
                # print(i.find('a').get('href'), i.get('class'))
                main_links_sub.append(URL[:-1] + i.find('a').get('href'))

    data_list = []
    for link in main_links:
        soup = Scraper.get_soup(link)
        total_pages = get_pagination(soup)
        data_list += get_data(soup)

        if total_pages != 1:
            for page in range(2, total_pages+1):
                soup = Scraper.get_soup(link+'page-'+str(page))
                data_list += get_data(soup)

    write_csv_in_file(data_list)


if __name__ == '__main__':
    main()
