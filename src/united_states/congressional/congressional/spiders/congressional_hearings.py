import scrapy
import json
import os
from congressional.items import CongressionalItemHearings
from congressional.pipelines import ReadArticles
from scrapy.utils.project import get_project_settings

GOV_INFO_API_KEY = get_project_settings().get('GOV_INFO_API_KEY')

class CongressionalHearingsSpider(scrapy.Spider):
    name = "congressional_hearings"
    allowed_domains = ["api.govinfo.gov"]
    start_urls = [f"https://api.govinfo.gov/collections/CHRG/2022-01-01T06%3A25%3A40Z?pageSize=100&offsetMark=%2A&api_key={GOV_INFO_API_KEY}"]

    def parse(self, response):
        data = json.loads(response.body)
        for package in data['packages']:
            scrapped = ReadArticles().check_item('congressional_hearings', package['packageId'], package['lastModified'])
            if scrapped == False:
                item_id = package['packageId']
                yield response.follow(f'https://api.govinfo.gov/packages/{item_id}/summary?api_key={GOV_INFO_API_KEY}', callback=self.parse_item)
    
    def parse_item(self, response):
        data = json.loads(response.body)
        item = CongressionalItemHearings()
        item = {
            'document_type': data.get('documentType'),
            'congress': data.get('congress'),
            'held_dates': data.get('heldDates'),
            'session': data.get('session'),
            'document_number': data.get('documentNumber'),
            'url': data.get('detailsLink'),
            'title': data.get('title'),
            'branch': data.get('branch'),
            'collection_name': data.get('collectionName'),
            'download': data.get('download'),
            'pages': data.get('pages'),
            'chamber': data.get('chamber'),
            'related_url': data.get('relatedLink'),
            'su_doc_class_number' : data.get('suDocClassNumber'),
            'granules_url': data.get('granulesLink'),
            'date_issued': data.get('dateIssued'),
            "package_id": data.get('packageId'),
            'collection_code': data.get('collectionCode'),
            'government_author1': data.get('governmentAuthor1'),
            'government_author2': data.get('governmentAuthor2'),
            'publisher': data.get('publisher'),
            'doc_class': data.get('docClass'),
            'created_at': data.get('lastModified'),
            'category': data.get('category'),
            'other_identifiers': data.get('otherIdentifier')
        }
        yield item