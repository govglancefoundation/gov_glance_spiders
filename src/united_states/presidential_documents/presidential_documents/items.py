# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PresidentialDocumentsItem(scrapy.Item):
    date_issued = scrapy.Field()
    issue = scrapy.Field()
    document_type = scrapy.Field()
    subject = scrapy.Field(serializer=list)
    package_id = scrapy.Field()
    collection_code = scrapy.Field()
    details_link = scrapy.Field()
    title = scrapy.Field()
    branch = scrapy.Field()
    collection_name = scrapy.Field()
    volumn = scrapy.Field()
    download = scrapy.Field(serailizer=dict)
    pages = scrapy.Field()
    government_author1 = scrapy.Field()
    government_author2 = scrapy.Field()
    publisher = scrapy.Field()
    doc_class = scrapy.Field()
    created_at = scrapy.Field()
    category = scrapy.Field()
    other_identifiers = scrapy.Field(serializer=dict)
    dcpd_category = scrapy.Field(serializer=list)
    president = scrapy.Field(serializer=dict)
    president_name = scrapy.Field()


