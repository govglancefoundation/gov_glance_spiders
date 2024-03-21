# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AgenciesItem(scrapy.Item):
    
    url = scrapy.Field()
    title = scrapy.Field()
    created_at = scrapy.Field()
    image = scrapy.Field()
    type = scrapy.Field()
    code = scrapy.Field()
    collection_name = scrapy.Field()
    description = scrapy.Field()

