from module import timer, Scraper, write_csv_in_file

URL = 'https://vologda.upravdom.com'
SHOW_50 = '?show=50'
PAGE = '&PAGEN_1='


def get_pagination(soup):
    try:
        total_pages = soup.find('ul', class_='pagination').find_all('li')

        if total_pages[-1].get('title') == 'Последняя страница':
            total_pages = total_pages[-1].find('a').get('href').split('=')[-1]
            total_pages = int(total_pages)
        else:
            total_pages = total_pages[-2].find('a').get('href').split('=')[-1]
            total_pages = int(total_pages)
    except AttributeError:
        total_pages = 1
        return total_pages
    return total_pages


def get_data(soup, title='УправДом', available='В наличии'):
    soup_items = soup.find('div', class_='catalog').find('div', class_='category-items').find_all('li', class_='item-wrapper')
    data_items = []

    for item in soup_items:
        name = item.find('span', itemprop='name').text.split()
        name = ' '.join(name)

        url = URL + item.find('a', itemprop='url').get('href')

        url_image = item.find('div', class_='image-wrapper').find('img').get('src')
        url_image = URL + url_image

        price = item.find('div', class_='new-price').text.split()
        price = ' '.join(price)

        data_item = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url, 'url_image': url_image}
        data_items.append(data_item)

    return data_items


@timer
def main():
    soup = Scraper.get_soup(URL)
    soup_data = soup.find('div', class_='main-container').find_all('div', class_='container')[1].find_all('div', 'col-sm-6')
    main_links = (URL + link.find('a').get('href') + SHOW_50 for link in soup_data)

    data_list = []
    for link in main_links:
        soup = Scraper.get_soup(link)
        total_pages = get_pagination(soup)
        data_list += get_data(soup)

        if total_pages != 1:
            for page in range(2, total_pages+1):
                soup = Scraper.get_soup(link+PAGE+str(page))
                data_list += get_data(soup)

    write_csv_in_file(data_list)
    print('Собрано данных: {}'.format(len(data_list)))


if __name__ == '__main__':
    main()
