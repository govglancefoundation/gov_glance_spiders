# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UsStatesSupremeCourtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    court_listener_id = scrapy.Field()
    title = scrapy.Field()
    created_at = scrapy.Field()
    url =  scrapy.Field()
    date_modified = scrapy.Field()
    download_link = scrapy.Field()
    clusters = scrapy.Field()
    cluster_id = scrapy.Field()
    opinion_api_link = scrapy.Field()
    judge_name = scrapy.Field()
    opinions_url = scrapy.Field()
    audio_files = scrapy.Field()
    description = scrapy.Field()
    


