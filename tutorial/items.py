# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MacappItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    icon = scrapy.Field()
    date_upload = scrapy.Field()
    category = scrapy.Field()
    screenshots = scrapy.Field()
    price = scrapy.Field()
    developer = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    download_link = scrapy.Field()
    slug = scrapy.Field()
