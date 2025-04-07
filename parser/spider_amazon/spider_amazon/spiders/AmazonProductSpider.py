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
    # new 
    # start_urls = [f'https://www.amazon.com/s?k=phone&i=mobile&rh=n%3A2335752011%2Cp_123%3A110955%257C146762%257C237204%257C254407%257C319106%257C329744%257C338933%257C358874%257C46655%257C473637%257C568349%2Cp_n_condition-type%3A6503240011&dc&page={i}&crid=VZIBEAHXCXRG&qid=1743764339&rnid=6503239011&sprefix=phone%2Caps%2C284&ref=sr_nr_p_n_condition-type_2&ds=v1%3AIjU2c0aUxE7Fr3xd9RvYh7NTIfZ3Ow3sQTENlKK2Ook' for i in range(1, 57)]
    # renewed. Их нужно переключать и определять файл куда они записываются в команде scrapy.crawl
    start_urls = [f'https://www.amazon.com/s?k=phone&i=mobile&rh=n%3A2335752011%2Cp_123%3A110955%257C146762%257C237204%257C254407%257C319106%257C329744%257C338933%257C358874%257C46655%257C473637%257C568349%2Cp_n_condition-type%3A16907722011&dc&page={i}&crid=VZIBEAHXCXRG&qid=1743771507&rnid=6503239011&sprefix=phone%2Caps%2C284&ref=sr_nr_p_n_condition-type_1&ds=v1%3AbQUafN4x2egXTwTGw1Kzw502jYnIsrq3cz2wQ1UYfqQ' for i in range(1, 36)]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url= get_url(url), callback=self.parse_main_page)


    def parse_main_page(self, response):
        product_urls = response.xpath('//div[contains(@class, "a-section a-spacing-small")]//a[@class="a-link-normal s-line-clamp-4 s-link-style a-text-normal"]/@href').getall()
        # product_urls = [link.get_attribute('href') for link in links]
        base_url = "https://www.amazon.com"
        full_urls = [base_url + url if url.startswith("/") else url for url in product_urls]
        for url in full_urls:
            yield scrapy.Request(url = get_url(url), callback=self.parse_phone)

    def get_tech_feature(self, response, field_name):
        return response.xpath(f'//th[contains(text(), "{field_name}")]/following-sibling::td//text()').get(default='Sorry bro').strip()



    def parse_phone(self, response):
        item = SpiderAmazonItem()
        
        item['phone_full_name'] = response.xpath('//h1[@id="title"]/span/text()').get(default='Sorry bro').strip()
        item['phone_review_rating'] = response.xpath('//span[@id="acrPopover"]/span[@class="a-declarative"]/a/span/text()').get(default='Sorry bro').strip()
        item['phone_rate_number'] = response.xpath('//span[@id="acrCustomerReviewText"]/text()').get(default='Sorry bro').strip()

        # Попытка 1: Стандартный способ (priceToPay)
        price_whole = response.xpath('//span[contains(@class, "priceToPay")]//span[@class="a-price-whole"]/text()').get()
        price_fraction = response.xpath('//span[contains(@class, "priceToPay")]//span[@class="a-price-fraction"]/text()').get()

        if price_whole and price_fraction:
            item['phone_sale_price'] = f"${price_whole.strip()}.{price_fraction.strip()}"
        else:
            # Попытка 2: Альтернативная структура (apexPriceToPay)
            sale_price_alt = response.xpath('//span[contains(@class, "apexPriceToPay")]//span[@class="a-offscreen"]/text()').get()
            item['phone_sale_price'] = sale_price_alt.strip() if sale_price_alt else 'Not available'

        list_price = response.xpath('//span[@class="a-price a-text-price"]//span[@class="a-offscreen"]/text()').get()
        if not list_price:
            # Альтернативная структура (в таблице)
            list_price = response.xpath('//td[contains(text(), "List Price:")]/following-sibling::td//span[@class="a-offscreen"]/text()').get()
        item['phone_list_price'] = list_price.strip() if list_price else 'Sorry bro'

    
        
        discount = response.xpath(
            '//span[contains(@class, "savingsPercentage")]/text() | '
            '//span[contains(@class, "savingsPercentage")]/preceding::span[contains(@class, "aok-offscreen")][1]/text()'
        ).re_first(r'(\d+)%')

        if not discount:
            # Попытка 2: Альтернативный блок скидок (если есть)
            discount = response.xpath('//td[contains(text(), "List Price:")]/following-sibling::td//span[contains(@class, "a-price")]/following-sibling::span/text()').re_first(r'(\d+)%')

        item['phone_discount'] = str(discount or '0') + '%'

        item['phone_brand'] = response.xpath('//tr[contains(@class, "po-brand")]/td[@class="a-span9"]/span/text()').get(default='Sorry bro').strip()

        # other tech info
        item['phone_dim'] = self.get_tech_feature(response, 'Product Dimensions')
        item['phone_weight'] = self.get_tech_feature(response, 'Item Weight')
        item['phone_ASIN'] = self.get_tech_feature(response, 'ASIN')
        item['phone_model_numer'] = self.get_tech_feature(response, 'Item model number')
        item['phone_batteries'] = self.get_tech_feature(response, 'Batteries')
        item['phone_os'] = self.get_tech_feature(response, 'OS')
        item['phone_ram'] = self.get_tech_feature(response, 'RAM')
        item['phone_wire_com_tech'] = self.get_tech_feature(response, 'Wireless communication technologies')
        item['phone_conn_tech'] = self.get_tech_feature(response, 'Connectivity technologies')
        item['phone_is_GPS'] = self.get_tech_feature(response, 'GPS')
        item['phone_special_features'] = self.get_tech_feature(response, 'Special features')
        item['phone_display_tech'] = self.get_tech_feature(response, 'Display technology')
        item['phone_other_display_features'] = self.get_tech_feature(response, 'Other display features')
        item['phone_human_int_input'] = self.get_tech_feature(response, 'Human Interface Input')
        item['phone_scanner_res'] = self.get_tech_feature(response, 'Scanner Resolution')
        item['phone_other_cam_features'] = self.get_tech_feature(response, 'Other camera features')
        item['phone_from_factor'] = self.get_tech_feature(response, 'Form Factor')
        item['phone_color'] = self.get_tech_feature(response, 'Color')
        item['phone_batt_power_rating'] = self.get_tech_feature(response, 'Battery Power Rating')
        item['phone_set'] = self.get_tech_feature(response, "Whats in the box")
        item['phone_manufacturer'] = self.get_tech_feature(response, 'Manufacturer')
        item['phone_date'] = self.get_tech_feature(response, 'Date First Available')
        item['phone_mem_storage_cap'] = self.get_tech_feature(response, 'Memory Storage Capacity')
        item['phone_standing_screen_display_size'] = self.get_tech_feature(response, 'Standing screen display size')
        item['phone_ram_memory_installed_size'] = self.get_tech_feature(response, 'Ram Memory Installed Size')


        # reviews
        for i in range(5, 0, -1):
            percent = response.xpath(f'//a[contains(@aria-label, "{i} percent of reviews")]/div[last()]/text()').get(default='Sorry bro')
            item[f'phone_cust_rev_{i}_perc'] = percent

            phone_cust_say = {}
    
        # tags
        aspects = response.xpath('//div[@aria-label="Commonly Mentioned Aspects"]/a')
        
        for aspect in aspects:
            aspect_name = aspect.xpath('./text()').get(default='Sorry bro').strip()
            
            data_item = aspect.xpath('./@data-csa-c-item-id').get(default='Sorry bro')
            tone = data_item.split('_')[-1] if data_item else 'UNKNOWN'
            
            bottom_sheet = response.xpath(
                f'//div[@data-aspect="{aspect_name}" '
                'or contains(@data-aspect, substring-before(@data-aspect, " "))]'
            )
            
            pos_rev = bottom_sheet.xpath(
                './/span[contains(@class, "text-positive")]/text()'
            ).re_first(r'\d+') or '0'
            
            neg_rev = bottom_sheet.xpath(
                './/span[contains(@class, "text-negative")]/text()'
            ).re_first(r'\d+') or '0'
            
            phone_cust_say[aspect_name] = {
                'pos_rev': pos_rev,
                'neg_rev': neg_rev,
                'tone': tone
            }
        
        item['phone_cust_say'] = phone_cust_say

        yield item