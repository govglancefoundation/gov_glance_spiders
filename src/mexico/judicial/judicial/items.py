# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JudicialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class SupremeCourtNewsroomItem(scrapy.Item):
    
    title = scrapy.Field()
    url = scrapy.Field()
    created_at = scrapy.Field()
    post_number = scrapy.Field()
    description = scrapy.Field()
    collection_name = scrapy.Field()