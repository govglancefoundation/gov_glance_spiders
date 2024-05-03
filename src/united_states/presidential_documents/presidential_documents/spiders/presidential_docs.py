import scrapy
import json
from presidential_documents.pipelines import ReadArticles
from presidential_documents.items import PresidentialDocumentsItem
from scrapy.utils.project import get_project_settings

GOV_INFO_API_KEY = get_project_settings().get('GOV_INFO_API_KEY')

class PresidentialDocsSpider(scrapy.Spider):
    name = "presidential_docs"
    allowed_domains = ["api.govinfo.gov"]
    start_urls = [f"https://api.govinfo.gov/collections/CPD/1700-01-28T20%3A18%3A10Z?pageSize=1000&offsetMark=%2A&api_key={GOV_INFO_API_KEY}"]

    def parse(self, response):
        data = json.loads(response.body)
        for package in data['packages']:
            # scrapped = ReadArticles().check_item('presidential_docs', package['packageId'], package['lastModified'])
            scrapped = False
            if scrapped == False:
                item_id = package['packageId']
                yield response.follow(f'https://api.govinfo.gov/packages/{item_id}/summary?api_key={GOV_INFO_API_KEY}', callback=self.parse_item)
        if data.get('nextPage'):
            yield response.follow(data['nextPage']+f'&api_key={GOV_INFO_API_KEY}', callback=self.parse)

    def parse_item(self, response):
        data = json.loads(response.body)
        item = PresidentialDocumentsItem()
        president = data.get('president')
        item = {
            'date_issued': data.get('dateIssued'),
            'issue': data.get('issue'),
            'document_type': data.get('documentType'),
            'subject': data.get('subject'),
            'package_id': data.get('packageId'),
            'collection_code': data.get('collectionCode'),
            'details_link': data.get('detailsLink'),
            'title': data.get('title'),
            'branch': data.get('branch'),
            'collection_name': data.get('collectionName'),
            'download': data.get('download'),
            'pages': data.get('pages'),
            'government_author1': data.get('governmentAuthor1'),
            'government_author2': data.get('governmentAuthor2'),
            'publisher': data.get('publisher'),
            'doc_class': data.get('docClass'),
            'created_at': data.get('lastModified'),
            'category': data.get('category'),
            'other_identifiers': data.get('otherIdentifier'),
            'dcpd_category': data.get('dcpdCategory'),
        }

        item['president'] = president
        if president:
            item['president_name'] = president['names'][1]['authority-fnf']
        yield item