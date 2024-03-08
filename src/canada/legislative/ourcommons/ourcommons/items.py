# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CommitteesItem(scrapy.Item):
    # define the fields for your item here like:
    # MEETING INFO
    title = scrapy.Field()
    code = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()
    created_at = scrapy.Field()
    start_at = scrapy.Field()
    end_at = scrapy.Field()
    address = scrapy.Field()
    address_url = scrapy.Field()
    stream_url = scrapy.Field()
    parliment = scrapy.Field()
    session = scrapy.Field()
    meeting_num = scrapy.Field()
    url = scrapy.Field()
    collection_name = scrapy.Field()
    home_url = scrapy.Field()