import scrapy
from urllib.parse import urlencode
from spider_amazon.items import SpiderAmazonItem

import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

API = os.getenv('SCRAPER_API_KEY')  # Получаем ключ

def get_url(url):
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload) # обращаемся к ScraperAPI, указывая необходимый сайт и API ключ
    return proxy_url

class AmazonproductspiderSpider(scrapy.Spider):
    name = 'AmazonProductSpider'
    allowed_domains = ['amazon.com', 'scraperapi.com']
    start_urls = ['https://www.amazon.com/dp/B00JES3MO0', 'https://www.amazon.com/dp/B08NCC24HV',
                  'https://www.amazon.com/dp/B09LCDF2VD', 'https://www.amazon.com/dp/B0B3D8Z7T8']

    def start_requests(self): # придется переписать start_requests - функция, которая работает с GET-запросами
        for url in self.start_urls:
            yield scrapy.Request(url=get_url(url), callback=self.parse)

    # Как эта функция выглядит по дефолту
        # def start_requests(self):
        # if not self.start_urls and hasattr(self, 'start_url'):
        #     raise AttributeError(
        #         "Crawling could not start: 'start_urls' not found "
        #         "or empty (but found 'start_url' attribute instead, "
        #         "did you miss an 's'?)")
        # for url in self.start_urls:
        #     yield Request(url, dont_filter=True)

    def parse(self, response):
        items = SpiderAmazonItem()
        title = response.xpath('//h1[@id="title"]/span/text()').extract()
        sale_price = response.xpath('//span[contains(@id,"swatch_price") or contains(@id,"saleprice")]/text()').extract()
        category = response.xpath('//a[@class="a-link-normal a-color-tertiary"]/text()').extract()
        availability = response.xpath('//div[@id="availability"]//text()').extract()
        items['product_name'] = ''.join(title).strip()
        items['product_sale_price'] = ''.join(sale_price).strip()
        items['product_category'] = ','.join(map(lambda x: x.strip(), category)).strip()
        items['product_availability'] = ''.join(availability).strip()
        yield items