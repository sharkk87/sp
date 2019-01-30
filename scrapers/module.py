import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import csv
import time
import os
import sys


from bs4 import BeautifulSoup
from datetime import datetime


class Scraper:

    @staticmethod
    def get_soup(url, verify=True):
        if verify:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'lxml')
            return soup
        else:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            html = requests.get(url, verify=verify)
            soup = BeautifulSoup(html.text, 'lxml')
            return soup

    @staticmethod
    def write_csv(name, data_list):
        with open(name, 'w') as file:
            writer = csv.writer(file)
            [writer.writerow((data['title'],
                              data['name'],
                              data['price'],
                              data['available'],
                              data['url'],
                              data['url_image'])) for data in data_list]


def timer(func):
    def wrapper():
        print('<<<Start scraping shop at {}>>>'.format(datetime.now()))
        start = time.time()
        func()
        end = time.time()
        total = end - start
        print('<<<Stop scraping. Total time: {:.2f} minutes>>>'.format(total/60))
    return wrapper


def get_data():
    date = datetime.today().strftime('%d%m%Y')
    return date


def get_name():
    name = os.path.basename(sys.argv[0]).split('.')
    return name[0]


def write_csv_in_file(data_list):
    os.chdir('shop_csv')
    Scraper.write_csv('{}_{}.csv'.format(get_data(), get_name()), data_list)
