# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SupremecourtItem(scrapy.Item):
    # define the fields for your item here like:
    r = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    created_at = scrapy.Field()
    justice = scrapy.Field()
    docket_number = scrapy.Field()
    collection_name = scrapy.Field()

class SupremecourtArgumentItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    audio_url = scrapy.Field()
    pdf_url = scrapy.Field()
    created_at = scrapy.Field()
    docket_number = scrapy.Field()
    collection_name = scrapy.Field()