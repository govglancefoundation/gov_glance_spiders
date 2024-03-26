import scrapy
import json
import os
from congressional.pipelines import ReadArticles
from scrapy.utils.project import get_project_settings

GOV_INFO_API_KEY = get_project_settings().get('GOV_INFO_API_KEY')

class CongressionalBillsSpider(scrapy.Spider):
    name = "congressional_bills"
    allowed_domains = ["api.govinfo.gov"]
    start_urls = [f"https://api.govinfo.gov/collections/BILLS/2023-01-01T20%3A18%3A10Z?pageSize=1000&offsetMark=%2A&api_key={GOV_INFO_API_KEY}"]
    

    # need to get a list of packageId's from the api can compare them to our database. Yield a list and ten check which ones we do not have
    def parse(self, response):
        
        data = json.loads(response.body)
        for package in data['packages']:
            scrapped = ReadArticles().check_item('congressional_bills', package['packageId'], package['lastModified'])
            if scrapped == False:
                item_id = package['packageId']
                yield response.follow(f'https://api.govinfo.gov/packages/{item_id}/summary?api_key={GOV_INFO_API_KEY}', callback=self.parse_item)
        if 'nextPage' in data:
            yield response.follow(data['nextPage']+f'&api_key={GOV_INFO_API_KEY}', callback=self.parse) 
    def parse_item(self, response):
        data = json.loads(response.body)
        short_title = data.get('shortTitle')
        if short_title != None:
            title = short_title[0]['title'],
            title = title[0]
        else:
            title = data.get('title')

        yield {
            'origin_chamber': data.get('originChamber'),
            'url': data.get('detailsLink'),
            'branch': data.get('branch'),
            'congress': data.get('congress'),
            'is_private': data.get('isPrivate'),
            'long_title': data.get('title'),
            'title': title,
            'branch': data.get('branch'),
            'is_appropriation': data.get('isAppropriation'),
            'collection_name': data.get('collectionName'),
            'download': data.get('download'),
            'pages': data.get('pages'),
            'related': data.get('related'),
            'related_url': data.get('relatedLink'),
            'members': data.get('members'),
            'su_doc_class_number' : data.get('suDocClassNumber'),
            'date_issued': data.get('dateIssued'),
            'current_chamber': data.get('currentChamber'),
            'bill_version': data.get('billVersion'),
            'bill_type': data.get('billType'),
            'package_id': data.get('packageId'),
            'committees': data.get('committees'),
            'committee': data.get('committeeName'),
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
        