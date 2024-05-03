import scrapy
import json
import os
from congressional.pipelines import ReadArticles
from congressional.items import CongressionalItemDocuments
from scrapy.utils.project import get_project_settings

GOV_INFO_API_KEY = get_project_settings().get('GOV_INFO_API_KEY')

class CongressionalDocumentsSpider(scrapy.Spider):
    name = "congressional_documents"
    allowed_domains = ["api.govinfo.gov"]
    start_urls = [f"https://api.govinfo.gov/collections/CDOC/2024-01-01T06%3A25%3A40Z?pageSize=100&offsetMark=%2A&api_key={GOV_INFO_API_KEY}"]

    def parse(self, response):
        
        data = json.loads(response.body)
        for package in data['packages']:
            scrapped = ReadArticles().check_item('congressional_documents', package['packageId'], package['lastModified'])
            if scrapped == False:
                item_id = package['packageId']
                yield response.follow(f'https://api.govinfo.gov/packages/{item_id}/summary?api_key={GOV_INFO_API_KEY}', callback=self.parse_item)
    
    def parse_item(self, response):
        data = json.loads(response.body)
        item = CongressionalItemDocuments()
        item = {

            'document_type': data.get('documentType'),
            'congress': data.get('congress'),
            'session': data.get('session'),
            'document_number': data.get('documentNumber'),
            'url': data.get('detailsLink'),
            'title': data.get('title'),
            'branch': data.get('branch'),
            'collection_name': 'Congressional Documents',
            'collection_name_2': data.get('collectionName'),
            'download': data.get('download'), 
            'pages': data.get('pages'),
            'chamber': data.get('chamber'),
            'su_doc_class_number' : data.get('suDocClassNumber'),
            'serial_set': data.get('serialSet'),
            'date_issued': data.get('dateIssued'),
            'agency': data.get('agency'),
            'subjects': data.get('subjects'),
            'package_id': data.get('packageId'),
            'collection_code': data.get('collectionCode'),
            'parent_id': data.get('parentId'),
            'volume': data.get('volume'),
            'government_author1': data.get('governmentAuthor1'),
            'government_author2': data.get('governmentAuthor2'),
            'publisher': data.get('publisher'),
            'doc_class': data.get('docClass'),
            'created_at': data.get('lastModified'),
            'category': data.get('category'),
            'granules_url': data.get('granulesLink'),
            'other_identifiers': data.get('otherIdentifier')}
        yield item