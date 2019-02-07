import os, time

from module import Scraper, timer, write_csv_in_file
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")

BASEDIR = os.path.abspath(os.path.dirname(__file__))
URL = 'http://evrostroy.biz/'

driver = webdriver.Chrome(BASEDIR + '/chromedriver', chrome_options=chrome_options)
driver.get(URL)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
text = soup.find('div', class_='ev-select').text

co = len(driver.find_elements_by_xpath("//div[@class='catalog-menu']/*/li[@class='action']/following-sibling::li/a"))

for i in range(co):
    print(i, co)
    driver.find_element_by_class_name('catalog-menu-block').click()

    a = driver.find_elements_by_xpath("//ul[@class='first-level']/li[@class='action']/following-sibling::li/a")[i]

    print(a.get_attribute('href'))
    driver.execute_script("arguments[0].scrollIntoView();", a)
    a.click()

    for i in range(10):
        time.sleep(1)
        b = driver.find_element_by_xpath("//div[@class='pages']/a[@class='btn white next']")
        print(b.get_attribute('class'))
        driver.execute_script("arguments[0].scrollIntoView();", b)
        time.sleep(1)
        b.click()




driver.close()
driver.quit()
