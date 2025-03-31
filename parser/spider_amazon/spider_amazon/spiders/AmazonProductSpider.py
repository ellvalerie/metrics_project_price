import scrapy
from urllib.parse import urlencode
from spider_amazon.items import SpiderAmazonItem

import os
from dotenv import load_dotenv

# подгрузка api-ключа для парсинга
load_dotenv()  

API = os.getenv('SCRAPER_API_KEY')  

def get_url(url):
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload) # обращаемся к ScraperAPI, указывая необходимый сайт и API ключ
    return proxy_url

class AmazonproductspiderSpider(scrapy.Spider):
    name = 'AmazonProductSpider'
    allowed_domains = ['amazon.com', 'scraperapi.com']
    start_urls = ['https://www.amazon.com/s?k=phone&i=mobile&rh=n%3A2335752011%2Cp_123%3A110955%257C146762%257C254407%257C319106%257C338933%257C46655%257C473637%257C568349&dc&ds=v1%3AiN%2BjkmQH4ZujsIKhRuowoS%2BjOBKjFWcPI%2FpUaNkQv5Q&crid=VZIBEAHXCXRG&qid=1743404738&rnid=85457740011&sprefix=phone%2Caps%2C284&ref=sr_nr_p_123_13']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=get_url(url), callback=self.parse_main_page)


    def parse_main_page(self, response):
        product_urls = response.xpath('//div[contains(@class, "a-section a-spacing-small")]//a[@class="a-link-normal s-line-clamp-4 s-link-style a-text-normal"]/@href').getall()
        # product_urls = [link.get_attribute('href') for link in links]
        base_url = "https://www.amazon.com"
        full_urls = [base_url + url if url.startswith("/") else url for url in product_urls]
        for url in full_urls:
            yield scrapy.Request(url=get_url(url), callback=self.parse_phone)

    def parse_phone(self, response):
        items = SpiderAmazonItem()
        
        items['phone_full_name'] = response.xpath('//h1[@id="title"]/span/text()').get(default='Не найдено').strip()
        items['phone_review_rating'] = response.xpath('//span[@id="acrPopover"]/span[@class="a-declarative"]/a/span/text()').get(default='Не найдено').strip()
        items['phone_rate_number'] = response.xpath('//span[@id="acrCustomerReviewText"]/text()').get(default='Не найдено').strip()
        
        price_whole = response.xpath('//span[@class="a-price-whole"]/text()').get()
        price_fraction = response.xpath('//span[@class="a-price-fraction"]/text()').get()
        if price_whole is None:
            items['phone_sale_price'] = 'Не найдено'
        else:
            price_whole = price_whole.strip() if price_whole else ''
            price_fraction = price_fraction.strip() if price_fraction else ''
            items['phone_sale_price'] = price_whole + price_fraction

        
        items['phone_list_price'] = response.xpath('//span[@class="a-price a-text-price"]//span[@class="a-offscreen"]/text()').get(default='Не найдено').strip()
        items['phone_discount'] = response.xpath('//span[contains(@class, "savingsPercentage")]/text()').get(default='Не найдено').strip()
        
        items['phone_brand'] = response.xpath('//tr[contains(@class, "po-brand")]/td[@class="a-span9"]/span/text()').get(default='Не найдено').strip()
        items['phone_operating_system'] = response.xpath('//tr[contains(@class, "po-operating_system")]/td[@class="a-span9"]/span/text()').get(default='Не найдено').strip()
        items['phone_ram_memory_size'] = response.xpath('//tr[contains(@class, "po-ram_memory.installed_size")]/td[@class="a-span9"]/span/text()').get(default='Не найдено').strip()
        items['phone_memory_storage_capacity'] = response.xpath('//tr[contains(@class, "po-memory_storage_capacity")]/td[@class="a-span9"]/span/text()').get(default='Не найдено').strip()
        items['phone_screen_size'] = response.xpath('//tr[contains(@class, "po-display.size")]/td[@class="a-span9"]/span/text()').get(default='Не найдено').strip()
        items['phone_model_name'] = response.xpath('//tr[contains(@class, "po-model_name")]/td[@class="a-span9"]/span/text()').get(default='Не найдено').strip()
        items['phone_resolution'] = response.xpath('//tr[contains(@class, "po-resolution")]/td[@class="a-span9"]/span/text()').get(default='Не найдено').strip()
        items['phone_cell_tech'] = response.xpath('//tr[contains(@class, "po-cellular_technology")]/td[@class="a-span9"]/span/text()').get(default='Не найдено').strip()
        
        yield items