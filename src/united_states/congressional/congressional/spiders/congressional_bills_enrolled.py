import scrapy
import json
from congressional.pipelines import ReadArticles
from congressional.items import CongressionalItemEnrolled
from scrapy.utils.project import get_project_settings

GOV_INFO_API_KEY = get_project_settings().get('GOV_INFO_API_KEY')

class CongressionalBillsEnrolledSpider(scrapy.Spider):
    name = "congressional_bills_enrolled"
    allowed_domains = ["api.govinfo.gov"]
    start_urls = [f"https://api.govinfo.gov/collections/BILLS/2022-01-17T06%3A25%3A40Z?pageSize=100&billVersion=enr&offsetMark=%2A&api_key={GOV_INFO_API_KEY}"]

    def parse(self, response):
        data = json.loads(response.body)
        for package in data['packages']:
            scrapped = ReadArticles().check_item('congressional_bills_enrolled', package['packageId'], package['lastModified'])
            
            if scrapped == False:
                item_id = package['packageId']
                yield response.follow(f'https://api.govinfo.gov/packages/{item_id}/summary?api_key={GOV_INFO_API_KEY}', callback=self.parse_item)
    
    def parse_item(self, response):
        data = json.loads(response.body)
        item = CongressionalItemEnrolled()
        item = {
            'branch': data.get('branch'),
            'origin_chamber': data.get('originChamber'),
            'congress': data.get('congress'),
            'session': data.get('session'),
            'url': data.get('detailsLink'),
            'is_private': data.get('isPrivate'),
            'title': data.get('title'),
            'is_appropriation': data.get('isAppropriation'),
            'collection_name': data.get('collectionName') +' Enrolled',
            'download': data.get('download'),
            'pages': data.get('pages'),
            'related': data.get('related'),
            'related_url': data.get('relatedLink'),
            'su_doc_class_number' : data.get('suDocClassNumber'),
            'date_issued': data.get('dateIssued'),
            'current_chamber': data.get('currentChamber'),
            'bill_version': data.get('billVersion'),
            'bill_type': data.get('billType'),
            'package_id': data.get('packageId'),
            'collection_code': data.get('collectionCode'),
            'government_author1': data.get('governmentAuthor1'),
            'government_author2': data.get('governmentAuthor2'),
            'publisher': data.get('publisher'),
            'doc_class': data.get('docClass'),
            'created_at': data.get('lastModified'),
            'category': data.get('category'),
            'bill_number': data.get('billNumber'),
            'other_identifiers': data.get('otherIdentifier')
        }
        yield item
