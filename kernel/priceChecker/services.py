from datetime import datetime
from multiprocessing import Process
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class ProductScraper:
    websites = {
        'https://www.euro.com.pl/search.bhtml?keyword={}' : 'parse_euro',
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
                if parser == 'parse_euro':
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.box-medium[_ngcontent-ng-c2960903584]')))
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                yield from getattr(self, parser)(soup, url)
        finally:
            driver.quit()

    def parse_media_expert(self, soup, url):
        offer = soup.select_one('div.offer-box')
        if offer:
            name = offer.select_one('a').text
            price = offer.select_one('span.whole').text
            link = offer.select_one('a')['href']
            raw_url = url.split('//')[1].split('/')[0]
            url = f'https://{raw_url}{link}'
            timestamp = datetime.now().isoformat()
            shop_name = 'Media Expert'
            yield {'name': name, 'price': price, 'shop_name': shop_name, 'url': url, 'timestamp': timestamp}

    def parse_x_kom(self, soup, url):
        offer = soup.select_one('div.sc-f5aee401-0')
        if offer:
            name = offer.select_one('h3.sc-99fda726-0 span').text
            price = offer.select_one('span.sc-fzqMAW').text
            link = offer.select_one('a')['href']
            raw_url = url.split('//')[1].split('/')[0]
            url = f'https://{raw_url}{link}'
            timestamp = datetime.now().isoformat()
            shop_name = 'X-Kom'
            yield {'name': name, 'price': price, 'shop_name': shop_name, 'url': url, 'timestamp': timestamp}
            
    def parse_euro(self, soup, url):
        offer = soup.select_one('div.box-medium')
        if offer:
            name = offer.select_one('a').text
            price = offer.select_one('span.price-template__large--total').text
            link = offer.select_one('a')['href']
            raw_url = url.split('//')[1].split('/')[0]
            url = f'https://{raw_url}{link}'
            timestamp = datetime.now().isoformat()
            shop_name = 'Euro RTV AGD'
            yield {'name': name, 'price': price, 'shop_name': shop_name, 'url': url, 'timestamp': timestamp}

    def parse_ceneo(self, soup, url):
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
            yield {'name': name, 'price': price, 'shop_name': shop_name, 'url': url, 'timestamp': timestamp}

    def parse_morele(self, soup, url):
        offer = soup.select_one('div.cat-product-content')
        if offer:
            name = offer.select_one('a').text
            price = offer.select_one('div.price-new').text
            link = offer.select_one('a')['href']
            raw_url = url.split('//')[1].split('/')[0]
            url = f'https://{raw_url}{link}'
            timestamp = datetime.now().isoformat()
            shop_name = 'Morele.net'
            yield {'name': name, 'price': price, 'shop_name': shop_name, 'url': url, 'timestamp': timestamp}
            
    def parse_komputronik(self, soup, url):
        offer = soup.select_one('div.tests-product-entry')
        if offer:
            name = offer.select_one('a').text
            price = offer.select_one('div.text-3xl').text
            link = offer.select_one('a.product-image')['href']
            url = f'{link}'
            timestamp = datetime.now().isoformat()
            shop_name = 'Komputronik'
            yield {'name': name, 'price': price, 'shop_name': shop_name, 'url': url, 'timestamp': timestamp}
    

def run_spider(product_name):
    scraper = ProductScraper()
    new_products = list(scraper.start_requests(product_name))

    try:
        with open('products.json', 'r') as f:
            products = json.load(f)
    except FileNotFoundError:
        products = []

    products.extend(new_products)

    with open('products.json', 'w') as f:
        json.dump(products, f)

def products_search_service(product_name):
    p = Process(target=run_spider, args=(product_name,))
    p.start()
    p.join()

    with open('products.json') as f:
        products = json.load(f)

    return products