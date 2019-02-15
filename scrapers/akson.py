import os
from time import sleep

from module import timer, write_csv_in_file

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

BASEDIR = os.path.abspath(os.path.dirname(__file__))
URL = 'https://m.akson.ru/c/'
CITY = '?TP_CITY_CODE=vologda'

chrome_options = Options()
# chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('window-size=1200,1100')

driver = webdriver.Chrome(BASEDIR + '/chromedriver', chrome_options=chrome_options)
# driver.implicitly_wait(10)


def check_class(name):
    try:
        driver.find_element_by_class_name(name)
        return True
    except NoSuchElementException:
        return False


@timer
def main():
    driver.get(URL + CITY)
    # driver.refresh()
    #
    # sleep(1)
    # driver.find_element_by_xpath("//div[@class='mobileContentContainer']/*/div[@class='leftFloat mobileListingSectionCaption']").click()

    # visited = {}
    def dfs(start):
        for i in range(len(start)):
            print(i, len(start), driver.find_elements_by_xpath("//li[@class='mobileCatalogListItem']")[i].text)
            # sleep(3)
            driver.find_elements_by_xpath("//li[@class='mobileCatalogListItem']")[i].click()
            dfs(driver.find_elements_by_xpath("//li[@class='mobileCatalogListItem']"))

        driver.find_element_by_xpath("//div[@class='mobileContentContainer']/*/div[@class='leftFloat mobileListingSectionCaption']").click()





    dfs(driver.find_elements_by_xpath("//li[@class='mobileCatalogListItem']"))




if __name__ == '__main__':
    main()



























# count = 0
# while count != len(driver.find_elements_by_xpath("//div[@class='mobileListingContainer']/div[@class='mobileListingItem']")):
#     count = len(driver.find_elements_by_xpath("//div[@class='mobileListingContainer']/div[@class='mobileListingItem']"))
#     add_data = driver.find_element_by_class_name('mobileListingLazyLoader')
#     driver.execute_script('arguments[0].scrollIntoView();', add_data)
#     add_data.click()
#     print(count)
#     sleep(1)
