# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CongressionalItem(scrapy.Item):
    # define the fields for your item here like:
    origin_chamber = scrapy.Field()
    created_at = scrapy.Field()
    title = scrapy.Field() # this title value will contain the short title.
    status_title = scrapy.Field() # combine bill number bill type ad bill version in the short title.
    branch = scrapy.Field()
    congress = scrapy.Field()
    session = scrapy.Field()
    url = scrapy.Field()
    short_title = scrapy.Field(serializer=list)
    is_private = scrapy.Field(serializer=bool)
    long_title = scrapy.Field()
    branch = scrapy.Field()
    is_appropriation = scrapy.Field(serializer=bool)
    collection_name = scrapy.Field()
    download = scrapy.Field(serializer=dict)
    pages = scrapy.Field()
    related = scrapy.Field(serializer=dict)
    related_url = scrapy.Field(serializer=list)
    members = scrapy.Field(serializer=list)
    su_doc_class_number = scrapy.Field()
    date_issed = scrapy.Field()
    current_chamber = scrapy.Field()
    bill_version = scrapy.Field()
    bill_type = scrapy.Field()  
    package_id = scrapy.Field()
    committee = scrapy.Field()
    committees = scrapy.Field(serializer=list)
    collection_code = scrapy.Field()
    government_author1 = scrapy.Field()
    government_author2 = scrapy.Field()
    publisher = scrapy.Field()
    doc_class = scrapy.Field()
    category = scrapy.Field()
    bill_number = scrapy.Field()
    other_identifiers = scrapy.Field(serializer=dict)
    parent_id = scrapy.Field()

class CongressionalItemEnrolled(scrapy.Item):
    origin_chamber = scrapy.Field()
    gov_info_references = scrapy.Field(serializer=list)
    congress = scrapy.Field()
    session = scrapy.Field()
    url = scrapy.Field()
    is_private = scrapy.Field(serializer=bool)
    title = scrapy.Field()
    branch = scrapy.Field()
    is_appropriation = scrapy.Field(serializer=bool)
    collection_name = scrapy.Field()
    download = scrapy.Field(serializer=dict)
    pages = scrapy.Field()
    related = scrapy.Field(serializer=dict)
    related_url = scrapy.Field()
    su_doc_class_number = scrapy.Field()
    date_issued = scrapy.Field()
    current_chamber = scrapy.Field()
    bill_version = scrapy.Field()
    bill_type = scrapy.Field()
    package_id = scrapy.Field()
    collection_code = scrapy.Field()
    government_author2 = scrapy.Field()
    government_author1 = scrapy.Field()
    publisher = scrapy.Field()
    doc_class = scrapy.Field()
    created_at = scrapy.Field()
    category = scrapy.Field()
    bill_number = scrapy.Field()
    other_identifiers = scrapy.Field(serializer=dict)
    status_title = scrapy.Field()

class CongressionalItemCommitteePrints(scrapy.Item):
    date_issued = scrapy.Field()
    document_type = scrapy.Field()
    congress = scrapy.Field()
    session = scrapy.Field()
    document_number = scrapy.Field()
    package_id = scrapy.Field()
    collection_code = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    branch = scrapy.Field()
    collection_name = scrapy.Field()
    download = scrapy.Field(serializer=dict)
    pages = scrapy.Field()
    government_author2 = scrapy.Field()
    chamber = scrapy.Field()
    government_author1 = scrapy.Field()
    publisher = scrapy.Field()
    su_doc_class_number = scrapy.Field()
    doc_class = scrapy.Field()
    created_at = scrapy.Field()
    category = scrapy.Field()
    other_identifiers = scrapy.Field(serializer=dict)
    granules_url = scrapy.Field()
    status_title = scrapy.Field()

class CongressionalItemDocuments(scrapy.Item):
    document_type = scrapy.Field()
    congress = scrapy.Field()
    session = scrapy.Field()
    document_number = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    branch = scrapy.Field()
    collection_name = scrapy.Field()
    download = scrapy.Field(serializer=dict)
    pages = scrapy.Field()
    chamber = scrapy.Field()
    su_doc_class_number = scrapy.Field()
    serial_set = scrapy.Field(serializer=dict)
    date_issued = scrapy.Field()
    agency = scrapy.Field()
    subjects = scrapy.Field(serializer=dict)
    package_id = scrapy.Field()
    collection_code = scrapy.Field()
    parent_id = scrapy.Field()
    volume = scrapy.Field()
    government_author2 = scrapy.Field()
    government_author1 = scrapy.Field()
    publisher = scrapy.Field()
    doc_class = scrapy.Field()
    created_at = scrapy.Field()
    category = scrapy.Field()
    other_identifier = scrapy.Field(serializer=dict)
    granules_url = scrapy.Field()
    status_title = scrapy.Field()

class CongressionalItemHearings(scrapy.Item):
    document_type = scrapy.Field()
    congress = scrapy.Field()
    held_dates = scrapy.Field(serializer=list)
    session = scrapy.Field()
    document_number = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    branch = scrapy.Field()
    collection_name = scrapy.Field()
    download = scrapy.Field(serializer=dict)
    pages = scrapy.Field()
    chamber = scrapy.Field()
    related_url = scrapy.Field()
    su_doc_class_number = scrapy.Field()
    granules_url = scrapy.Field()
    date_issued = scrapy.Field()
    package_id = scrapy.Field()
    collection_code = scrapy.Field()
    government_author2 = scrapy.Field()
    government_author1 = scrapy.Field()
    publisher = scrapy.Field()
    doc_class = scrapy.Field()
    last_modified = scrapy.Field()
    category = scrapy.Field()
    other_identifier = scrapy.Field(serializer=dict)
    status_title = scrapy.Field()

class CongressionalItemReports(scrapy.Item):
    document_type = scrapy.Field()
    congress = scrapy.Field()
    session = scrapy.Field()
    document_number = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    branch = scrapy.Field()
    collection_name = scrapy.Field()
    download = scrapy.Field(serializer=dict)
    pages = scrapy.Field()
    chamber = scrapy.Field()
    su_doc_class_number = scrapy.Field()
    serial_set = scrapy.Field(serializer=dict)
    date_issued = scrapy.Field()
    agency = scrapy.Field()
    subjects = scrapy.Field(serializer=dict)
    package_id = scrapy.Field()
    collection_code = scrapy.Field()
    parent_id = scrapy.Field()
    volume = scrapy.Field()
    government_author2 = scrapy.Field()
    government_author1 = scrapy.Field()
    publisher = scrapy.Field()
    doc_class = scrapy.Field()
    created_at = scrapy.Field()
    category = scrapy.Field()
    other_identifier = scrapy.Field(serializer=dict)
    granules_url = scrapy.Field()
    status_title = scrapy.Field()

class PublicPrivateLawsItem(scrapy.Item):
    date_issued = scrapy.Field()
    references = scrapy.Field(serializer=list)
    document_type = scrapy.Field()
    congress = scrapy.Field()
    document_number = scrapy.Field()
    package_id = scrapy.Field()
    collection_code = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    short_title = scrapy.Field()
    long_title = scrapy.Field()
    branch = scrapy.Field()
    collection_name = scrapy.Field()
    download = scrapy.Field(serializer=dict)
    pages = scrapy.Field()
    government_author2 = scrapy.Field()
    related_url = scrapy.Field()
    government_author1 = scrapy.Field()
    publisher = scrapy.Field()
    doc_class = scrapy.Field()
    created_at = scrapy.Field()
    category = scrapy.Field()
    other_identifier = scrapy.Field(serializer=dict)
    status_title = scrapy.Field()
