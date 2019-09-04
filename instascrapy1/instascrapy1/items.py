# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Instascrapy1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    date = scrapy.Field()
    like_count = scrapy.Field()
    explain = scrapy.Field()
    each_url = scrapy.Field()
    after = scrapy.Field()

