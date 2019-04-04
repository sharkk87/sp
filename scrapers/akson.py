import os
from time import sleep

from module import timer, write_csv_in_file
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

BASEDIR = os.path.abspath(os.path.dirname(__file__))
URL = 'https://m.akson.ru/c/'
CITY = '?TP_CITY_CODE=vologda'

BAD_URLS = ['Постер на заказ', 'Автотовары', 'Спецпредложения', 'Акции']

chrome_options = Options()
# chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')
chrome_options.add_argument('window-size=1200,1100')

driver = webdriver.Chrome(BASEDIR + '/chromedriver', chrome_options=chrome_options)
# driver.implicitly_wait(10)

data_list = []


def check_contains_class(name):
    try:
        driver.find_element_by_class_name(name)
        return True
    except NoSuchElementException:
        return False


def show_more():
    count = 0
    while count != len(driver.find_elements_by_xpath("//div[@class='mobileListingContainer']/div[@class='mobileListingItem']")):
        count = len(driver.find_elements_by_xpath("//div[@class='mobileListingContainer']/div[@class='mobileListingItem']"))
        print(count)

        try:
            add_data = driver.find_element_by_class_name('mobileListingLazyLoader')
            driver.execute_script('arguments[0].scrollIntoView();', add_data)
            add_data.click()
            sleep(2)
        except ElementNotVisibleException:
            pass


def dfs():
    len_items = len(driver.find_elements_by_xpath("//li[@class='mobileCatalogListItem']"))

    text = False
    for i in range(len_items):
        text = driver.find_elements_by_xpath("//li[@class='mobileCatalogListItem']")[i].text
        print(i+1, len_items, text)

        if text in BAD_URLS:
            print(text, 'This url contains bug')
            continue
        else:
            driver.find_elements_by_xpath("//li[@class='mobileCatalogListItem']")[i].click()

            if check_contains_class('mobileListingContainer'):
                show_more()
                get_data()

        dfs()

    if text == 'Спецпредложения':
        print('Finish')
    else:
        try:
            back = driver.find_element_by_xpath("//div[@class='mobileContentContainer']/*/div[@class='leftFloat mobileListingSectionCaption']")
            driver.execute_script('arguments[0].scrollIntoView();', back)
            driver.execute_script('scroll(0, -250);')
            back.click()
        except NoSuchElementException:
            print('Finish')
            driver.back()


def get_data():
    global data_list
    title = 'Аксон'

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    data = soup.find('div', class_='mobileListingContainer').find_all('div', class_='mobileListingItem')

    for item in data:
        name = item.find('div', class_='mobileListingItemName').text.split()
        name = ' '.join(name)

        url = item.find('div', class_='mobileListingItemName').find('a').get('href')
        url = 'https://akson.ru' + url + CITY

        url_image = item.find('div', class_='mobileListingItemImage').get('style').split('(')[1]
        url_image = url_image.replace("'", '')
        url_image = url_image.replace(");", '')

        price = item.find('span', class_='mobileListingItemPriceNumber').text

        try:
            available = item.find('span', class_='avail-sticker').text.capitalize()

            if available == 'Выставочный образец':
                available = 'В наличии'
        except AttributeError:
            available = 'Нет в наличии'

        data = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url, 'url_image': url_image}
        data_list.append(data)


@timer
def main():
    driver.get(URL + CITY)
    # driver.get('https://m.akson.ru/c/kley_plitochnyy/' + CITY)
    # driver.refresh()
    # get_data()
    # show_more()
    dfs()

    write_csv_in_file(data_list)
    print('Собрано данных: {}'.format(len(data_list)))


if __name__ == '__main__':
    try:
        main()
    finally:
        driver.close()
        driver.quit()
