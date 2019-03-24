import os

from module import timer, write_csv_in_file
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

BASEDIR = os.path.abspath(os.path.dirname(__file__))
URL = 'http://evrostroy.biz/'
CITY = '?sx_city=Вологда'

chrome_options = Options()
# chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')
chrome_options.add_argument('window-size=1200,1100')

driver = webdriver.Chrome(BASEDIR + '/chromedriver', chrome_options=chrome_options)
driver.implicitly_wait(10)

data_list = []


def check_contains_class(name):
    try:
        driver.find_element_by_class_name(name)
        return True
    except NoSuchElementException:
        return False


def get_data():
    global data_list
    title = 'Еврострой'

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    # print(soup.find('p', class_='cityPhone').text)

    data = soup.find('div', class_='catalog-items-list').find_all('div', class_='item-list-block')

    for item in data:
        name = item.find('div', class_='name').text.split()
        name = ' '.join(name)

        url = item.find('div', class_='name').find('a').get('href')
        url = URL[:-1] + url + CITY

        url_image = item.find('div', class_='img').get('style').split('"')[1]
        url_image = URL[:-1] + url_image

        try:
            price = item.find('div', class_='price').find('em').next_element.strip()
        except AttributeError:
            price = ''

        available = item.find('div', class_='to-basket').find('span', class_='add-to-basket-popup').previous_element
        if available == 'Заказать':
            available = 'Под заказ'
        elif available == 'В корзину':
            available = 'В наличии'

        data = {'title': title, 'name': name, 'price': price, 'available': available, 'url': url, 'url_image': url_image}
        data_list.append(data)


@timer
def main():
    driver.get(URL + CITY)
    print(driver.find_element_by_class_name('cityPhone').text)

    count_main_links = len(driver.find_elements_by_xpath("//div[@class='catalog-menu']/*/li[@class='action']/following-sibling::li/a"))

    for i in range(count_main_links):
        driver.find_element_by_class_name('catalog-menu-block').click()
        link = driver.find_elements_by_xpath("//ul[@class='first-level']/li[@class='action']/following-sibling::li/a")[i]
        url = link.get_attribute('href')

        driver.execute_script('arguments[0].scrollIntoView();', link)
        link.click()

        if check_contains_class('catalog-items-list'):
            button_next = driver.find_elements_by_xpath("//div[@class='pages']/a")[-2]
            disabled = button_next.get_attribute('class').split()[-1]

            get_data()

            while disabled == 'next':
                driver.execute_script("arguments[0].scrollIntoView();", button_next)
                button_next.click()

                button_next = driver.find_elements_by_xpath("//div[@class='pages']/a")[-2]
                disabled = driver.find_elements_by_xpath("//div[@class='pages']/a")[-2].get_attribute('class').split()[-1]

                get_data()
        else:
            print('No data this page: {}'.format(url))

    # Create csv-file and write data
    write_csv_in_file(data_list)
    print('Собрано данных: {}'.format(len(data_list)))


if __name__ == '__main__':
    try:
        main()
    finally:
        driver.close()
        driver.quit()
