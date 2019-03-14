from module import Scraper, timer, write_csv_in_file

URL = 'https://www.apline35.ru/catalog/'


@timer
def main():
    # Get object soup to BeautifulSoup
    soup = Scraper.get_soup(URL, False)

    # Get object's list
    main_object_links = soup.find('div', class_='sections').find_all('li', class_='section')

    # Get all links with int total pages - dict
    WWW = 'https://www.apline35.ru'
    DROP = '?alfaction=coutput&alfavalue=20'
    all_links = (WWW + href.find('a', class_='psection').get('href') + DROP for href in main_object_links)

    all_links_total = {}
    for link in all_links:
        soup = Scraper.get_soup(link, False)
        try:
            total = int(soup.find('div', class_='navigation').find_all('a')[-2].text)
        except IndexError:
            print('Don\'t find pagination in: {}'.format(link))
            total = 1

        all_links_total[link] = total

    # Go in all pages with scrap data into list
    data_list = []
    title = 'АПлайн'
    for page, total_page in all_links_total.items():
        #print(page, total_page)
        for link in range(1, total_page + 1):
            link_data = page + '&PAGEN_1=' + str(link)
            soup = Scraper.get_soup(link_data, False)

            try:
                data = soup.find('div', class_='showcase').find_all('div', class_='js-element')
            except AttributeError:
                print('No data on this page: {}'.format(link_data))
                continue

            for i in data:
                name = i.find('div', class_='name').text.split()
                name = ' '.join(name)

                url = i.find('div', class_='padd').find('a').get('href')
                url = 'http://www.apline35.ru' + url

                url_image = i.find('div', class_='pic').find('img').get('src')
                url_image = 'http://www.apline35.ru' + url_image

                price = i.find('div', class_='soloprice').text.strip()

                # available = i.find('div', class_='compare_and_stores').find('div', class_='stores').text.strip()
                available = 'В наличии'

                data = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url, 'url_image': url_image}
                data_list.append(data)

    # Create csv-file and write data
    write_csv_in_file(data_list)
    print('Собрано данных: {}'.format(len(data_list)))


if __name__ == '__main__':
    main()
