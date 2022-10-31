# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CasasbahiaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    description = scrapy.Field()
    specs = scrapy.Field()
    url_images = scrapy.Field()
    quanty_rating = scrapy.Field()
    user_reviews = scrapy.Field()
    delivery = scrapy.Field()
    payment_methods = scrapy.Field()
    breadcrumb = scrapy.Field()
    seller = scrapy.Field()
   