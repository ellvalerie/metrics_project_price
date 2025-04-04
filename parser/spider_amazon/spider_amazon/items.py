# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


# example of the phone page
# https://www.amazon.com/Apple-iPhone-12-64GB-Black/dp/B08PP5MSVB/ref=sr_1_4?crid=VZIBEAHXCXRG&dib=eyJ2IjoiMSJ9.v8-v_dYf_IhKGWbz-_aPp3-4XK2XRl11XHJjXy4WtEts9hsMpTtHPgwUXySFmwvpaGMdnRdIRhJv6rDOLU6vLvRpH-3oHG7Xuw7T0oFH5Qv8GmUVMIidwogAc_UVfIUnisd_a4dI7yZJsAw3X8w7kMJ3AilEeuVsYrMZRld0QU__BaSazppisql7jNYALwkJE1QMfswxnNkg5u-UHSI_MP84yQkVnqCo0YzLWcOk-fiSa-qw8pB5zBtuOsM0uJKPo1O5lNW9hjplbMxvWPBV64noJlFktO24pbp2RdXrstA.BQKoPe8jejsAwTEiUi_yQRR-OZXT7woz1LI0lf0Fn8A&dib_tag=se&keywords=phone&qid=1743759026&refinements=p_123%3A110955%7C146762%7C254407%7C319106%7C338933%7C46655%7C473637%7C568349&rnid=85457740011&s=wireless&sprefix=phone%2Caps%2C284&sr=1-4&th=1

import scrapy

class SpiderAmazonItem(scrapy.Item):
    # main info
    phone_full_name = scrapy.Field()
    phone_list_price = scrapy.Field()
    phone_sale_price = scrapy.Field()
    phone_discount = scrapy.Field()
    phone_review_rating = scrapy.Field()
    phone_rate_number = scrapy.Field()
    phone_brand = scrapy.Field()
    # other tech info
    phone_dim = scrapy.Field()
    phone_weight = scrapy.Field()
    phone_ASIN = scrapy.Field() # уникальный идетификатор каждого товара на амазон
    phone_model_numer = scrapy.Field()
    phone_batteries = scrapy.Field()
    phone_os = scrapy.Field()
    phone_ram = scrapy.Field()
    phone_wire_com_tech = scrapy.Field() # Wireless communication technologies
    phone_conn_tech = scrapy.Field() # Connectivity technologies
    phone_is_GPS = scrapy.Field()
    phone_special_features = scrapy.Field()
    phone_display_tech = scrapy.Field()
    phone_other_display_features = scrapy.Field()
    phone_human_int_input = scrapy.Field() # Human Interface Input
    phone_scanner_res = scrapy.Field() # Scanner Resolution
    phone_other_cam_features = scrapy.Field() # Other camera features
    phone_from_factor = scrapy.Field()
    phone_color = scrapy.Field()
    phone_batt_power_rating = scrapy.Field() # Battery Power Rating
    phone_set = scrapy.Field() # Whats in the box
    phone_manufacturer = scrapy.Field() 
    phone_date = scrapy.Field() # Date First Available
    phone_mem_storage_cap = scrapy.Field() # Memory Storage Capacity
    phone_standing_screen_display_size = scrapy.Field() # Standing screen display size
    phone_ram_memory_installed_size = scrapy.Field()
    # reviews 
    phone_cust_rev_5_perc = scrapy.Field()
    phone_cust_rev_4_perc = scrapy.Field()
    phone_cust_rev_3_perc = scrapy.Field()
    phone_cust_rev_2_perc = scrapy.Field()
    phone_cust_rev_1_perc = scrapy.Field()
    phone_cust_say = scrapy.Field() # dict {feature : {pos_rev : "num", neg_rev : "num", tone : "POSITIVE"/"NEGATIVE"/"MIXED"}

