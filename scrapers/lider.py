from module import Scraper, timer, write_csv_in_file

URL = 'https://lider35.ru/catalog/'
COUNT_80 = '?alfaction=coutput&alfavalue=80'
PAGE = '&PAGEN_1='


@timer
def main():
    # Get main links
    soup = Scraper.get_soup(URL)
    main_links_data = soup.find('ul', class_='category-list').children
    main_links = (URL[:18] + link.find('a').get('href') + COUNT_80 for link in main_links_data)

    # Fill dict links with int pagination
    links = {}
    for link in main_links:
        soup = Scraper.get_soup(link)

        try:
            page = int(soup.find('div', class_='modern-page-navigation').find_all('a', class_='number')[-1].text)
        except AttributeError:
            page = 1

        links[link] = page

    # Go to all page and fill list data
    title = 'Лидер'
    data_list = []
    for page, page_total in links.items():
        for page_num in range(1, page_total + 1):
            soup = Scraper.get_soup(page + PAGE + str(page_num))

            try:
                data = soup.find('div', class_='catalog-items').find_all('div', class_='catalog-item_inner')
            except AttributeError:
                print('No find data this page: {}'.format(page + PAGE + str(page_num)))
                continue

            for i in data:
                name = i.find('a', class_='text_fader').text.split()
                name = ' '.join(name)

                url = i.find('a', class_='qb_corner').get('href')
                url = 'https://lider35.ru' + url

                price = i.find('div', class_='price').text.strip()

                try:
                    available = i.find_all('div', class_='catalog-article')[1].get_text().strip()
                except:
                    available = i.find('div', class_='catalog-article-quantity').get_text().strip()

                data = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url}
                data_list.append(data)

    # Create csv-file and write data
    write_csv_in_file(data_list)
    print('Собрано данных: {}'.format(len(data_list)))


if __name__ == '__main__':
    main()
