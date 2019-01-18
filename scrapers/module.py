import requests
import csv
import time
import os
import sys


from bs4 import BeautifulSoup
from datetime import datetime


class Scraper:

    @staticmethod
    def get_soup(url, verify=True):
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
                              data['url'])) for data in data_list]


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
    os.chdir('shop')
    Scraper.write_csv('{}_{}.csv'.format(get_data(), get_name()), data_list)
