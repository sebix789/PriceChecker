from datetime import datetime
from selenium import webdriver
from pymongo import MongoClient
from bs4 import BeautifulSoup
from bson.regex import Regex

import environ

env = environ.Env()
environ.Env.read_env()

class ProductScraper:
    websites = {
        'https://www.ceneo.pl/szukaj-{}' : 'parse_ceneo',
        'https://www.morele.net/wyszukiwarka/?q={}&d=0' : 'parse_morele',
        'https://www.mediaexpert.pl/search?query[menu_item]=&query[querystring]={}': 'parse_media_expert',
        'https://www.komputronik.pl/search/category/1?query={}': 'parse_komputronik',
        'https://www.x-kom.pl/szukaj?q={}': 'parse_x_kom'
    }

    def start_requests(self, product_name):
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)
        try:
            for website, parser in self.websites.items():
                url = website.format(product_name)
                print(f"Visiting: {url}")
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                yield from getattr(self, parser)(soup, url, product_name)
        finally:
            driver.quit()

    def parse_media_expert(self, soup, url, product_name):
        offer = soup.select_one('div.offer-box')
        if offer:
            name = offer.select_one('a').text
            price = offer.select_one('span.whole').text
            link = offer.select_one('a')['href']
            raw_url = url.split('//')[1].split('/')[0]
            url = f'https://{raw_url}{link}'
            timestamp = datetime.now().isoformat()
            shop_name = 'Media Expert'
            keywords = product_name.split(' ')
            yield {'name': name, 'price': price, 'shop_name': shop_name, 'url': url, 'timestamp': timestamp, 
                   'keywords': keywords }

    def parse_x_kom(self, soup, url, product_name):
        offer = soup.select_one('div.sc-f5aee401-0')
        if offer:
            name = offer.select_one('h3.sc-99fda726-0 span').text
            price = offer.select_one('span.sc-fzqMAW').text
            link = offer.select_one('a')['href']
            raw_url = url.split('//')[1].split('/')[0]
            url = f'https://{raw_url}{link}'
            timestamp = datetime.now().isoformat()
            shop_name = 'X-Kom'
            keywords = product_name.split(' ')
            yield {'name': name, 'price': price, 'shop_name': shop_name, 'url': url, 'timestamp': timestamp,
                   'keywords': keywords}

    def parse_ceneo(self, soup, url, product_name):
        offer = soup.select_one('div.cat-prod-row')
        if offer:
            new_badge = offer.select_one('a span.new-label')
            if new_badge:
                name = offer.select_one('a span.font-bold').text
            else:
                name = offer.select_one('a span').text
            price = offer.select_one('span.price').text
            link = offer.select_one('a')['href']
            raw_url = url.split('//')[1].split('/')[0]
            url = f'https://{raw_url}{link}'
            timestamp = datetime.now().isoformat()
            shop_name = 'Ceneo.pl'
            keywords = product_name.split(' ')
            yield {'name': name, 'price': price, 'shop_name': shop_name, 'url': url, 'timestamp': timestamp,
                   'keywords': keywords}

    def parse_morele(self, soup, url, product_name):
        offer = soup.select_one('div.cat-product-content')
        if offer:
            name = offer.select_one('a').text
            price = offer.select_one('div.price-new').text
            link = offer.select_one('a')['href']
            raw_url = url.split('//')[1].split('/')[0]
            url = f'https://{raw_url}{link}'
            timestamp = datetime.now().isoformat()
            shop_name = 'Morele.net'
            keywords = product_name.split(' ')
            yield {'name': name, 'price': price, 'shop_name': shop_name, 'url': url, 'timestamp': timestamp,
                   'keywords': keywords}
            
    def parse_komputronik(self, soup, url, product_name):
        offer = soup.select_one('div.tests-product-entry')
        if offer:
            name = offer.select_one('a').text
            price = offer.select_one('div.text-3xl').text
            link = offer.select_one('a.product-image')['href']
            url = f'{link}'
            timestamp = datetime.now().isoformat()
            shop_name = 'Komputronik'
            keywords = product_name.split(' ')
            yield {'name': name, 'price': price, 'shop_name': shop_name, 'url': url, 'timestamp': timestamp,
                   'keywords': keywords}
    

def run_spider(product_name):
    scraper = ProductScraper()
    new_products = list(scraper.start_requests(product_name))
    
    client = MongoClient(env('MONGO_URI'))
    db = client[env('DB_NAME')]
    collection = db['products']

    collection.insert_many(new_products)

def products_search_service(product_name):    
    client = MongoClient(env('MONGO_URI'))
    db = client[env('DB_NAME')]
    collection = db['products']
    
    keywords = product_name.split()
    
    products = list(collection.find({'keywords': {'$all': keywords}}))
    
    if not products:
        run_spider(product_name)
        products = list(collection.find({'keywords': {'$all': keywords}}))
        
    for product in products:
        product['_id'] = str(product['_id'])

    return products

def shop_filter_service(shop_name):
    client = MongoClient(env('MONGO_URI'))
    db = client[env('DB_NAME')]
    collection = db['products']
    
    if shop_name == 'all':
        products = list(collection.find())
    else:
        products = list(collection.find({'shop_name': shop_name}))
    
    for product in products:
        product['_id'] = str(product['_id'])
        
    return products