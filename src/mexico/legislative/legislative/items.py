# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LegislativeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ChamberOfDeputiesNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image = scrapy.Field()
    created_at = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    collection_name = scrapy.Field()
    description = scrapy.Field()
    branch = scrapy.Field()
    topic = scrapy.Field()