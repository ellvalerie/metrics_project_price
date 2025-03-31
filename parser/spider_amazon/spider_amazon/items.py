# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html



import scrapy

class SpiderAmazonItem(scrapy.Item):
    phone_full_name = scrapy.Field()
    phone_list_price = scrapy.Field()
    phone_sale_price = scrapy.Field()
    phone_discount = scrapy.Field()
    phone_review_rating = scrapy.Field()
    phone_rate_number = scrapy.Field()
    phone_brand = scrapy.Field()
    phone_operating_system = scrapy.Field()
    phone_ram_memory_size = scrapy.Field()
    phone_memory_storage_capacity = scrapy.Field()
    phone_screen_size = scrapy.Field()
    phone_model_name = scrapy.Field()
    phone_resolution = scrapy.Field()
    phone_cell_tech = scrapy.Field()

