# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ExecutiveItemDOI(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    img = scrapy.Field()
    created_at = scrapy.Field()
    description = scrapy.Field()
    collection_name = scrapy.Field()
    table_name = scrapy.Field()

