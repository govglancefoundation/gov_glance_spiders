# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RepresentativesItem(scrapy.Item):
    citation = scrapy.Field()
    document_namer = scrapy.Field()
    end_page = scrapy.Field()
    url = scrapy.Field()
    pdf_url = scrapy.Field()
    doc_type = scrapy.Field()
    subtype = scrapy.Field()
    publication_date = scrapy.Field()
    signing_date = scrapy.Field()
    start_page = scrapy.Field()
    title = scrapy.Field()
    disposition_notes = scrapy.Field()
    executive_order_number = scrapy.Field()
    not_received_for_publication = scrapy.Field()
    full_text_xml_url = scrapy.Field()
    body_html_url = scrapy.Field()
    json_url = scrapy.Field()

class RepresentativesStateUnionItem(scrapy.Item):
    president = scrapy.Field()
    url = scrapy.Field()
    collection_name = scrapy.Field()
    title = scrapy.Field()
    created_at = scrapy.Field()
    description = scrapy.Field()
    notes = scrapy.Field()
    doc_type = scrapy.Field()
    subtype = scrapy.Field()
    executive_order_number = scrapy.Field()
   
