import scrapy
import json
from congressional.pipelines import ReadArticles
from congressional.items import CongressionalItemCommitteePrints
from scrapy.utils.project import get_project_settings

GOV_INFO_API_KEY = get_project_settings().get('GOV_INFO_API_KEY_SANTI')


class CongressionalCommitteePrintsSpider(scrapy.Spider):
    name = "congressional_committee_prints"
    allowed_domains = ["api.govinfo.gov"]
    start_urls = [f"https://api.govinfo.gov/collections/CPRT/1899-01-17T06%3A25%3A40Z?pageSize=100&offsetMark=%2A&api_key={GOV_INFO_API_KEY}"]

    def parse(self, response):
        
        data = json.loads(response.body)
        for package in data['packages']:
            scrapped = ReadArticles().check_item('congressional_committee_prints', package['packageId'], package['lastModified'])
            if scrapped == False:
                item_id = package['packageId']
                yield response.follow(f'https://api.govinfo.gov/packages/{item_id}/summary?api_key={GOV_INFO_API_KEY}', callback=self.parse_item, meta={'created_at': package['lastModified']})
        if data.get('nextPage'):
            yield response.follow(data['nextPage']+f'&api_key={GOV_INFO_API_KEY}', callback=self.parse)
    
    def parse_item(self, response):
        data = json.loads(response.body)
        items = CongressionalItemCommitteePrints()
        created_at = response.meta.get('created_at')
        items = {
            'date_issued': data.get('dateIssued'),
            'document_type': data.get('documentType'),
            'congress': data.get('congress'),
            'session': data.get('session'),
            'document_number': data.get('documentNumber'),
            'package_id': data.get('packageId'),
            'collection_code': data.get('collectionCode'),
            'url': data.get('detailsLink'),
            'title': data.get('title'),
            'branch': data.get('branch'),
            'collection_name': data.get('collectionName'),
            'download': data.get('download'),
            'pages': data.get('pages'),
            'chamber': data.get('chamber'),
            'su_doc_class_number' : data.get('suDocClassNumber'),
            'government_author2': data.get('governmentAuthor2'),
            'government_author1': data.get('governmentAuthor1'),
            'publisher': data.get('publisher'),
            'doc_class': data.get('docClass'),
            'created_at': created_at,
            'category': data.get('category'),
            'other_identifiers': data.get('otherIdentifier'),
            'granules_url': data.get('granulesLink'),
        }
        yield items