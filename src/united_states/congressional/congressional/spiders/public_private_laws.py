import scrapy
import json
from congressional.pipelines import ReadArticles
from congressional.items import PublicPrivateLawsItem
from scrapy.utils.project import get_project_settings

GOV_INFO_API_KEY = get_project_settings().get('GOV_INFO_API_KEY')


class PublicPrivateLawsSpider(scrapy.Spider):
    name = "public_private_laws"
    allowed_domains = ["api.govinfo.gov"]
    start_urls = [f"https://api.govinfo.gov/collections/PLAW/2022-01-17T06%3A25%3A40Z?pageSize=100&offsetMark=%2A&api_key={GOV_INFO_API_KEY}"]

    def parse(self, response):
        
        data = json.loads(response.body)
        for package in data['packages']:
            scrapped = ReadArticles().check_item('public_and_private_laws', package['packageId'], package['lastModified'])
            if scrapped == False:
                item_id = package['packageId']
                yield response.follow(f'https://api.govinfo.gov/packages/{item_id}/summary?api_key={GOV_INFO_API_KEY}', callback=self.parse_item)

    
    def parse_item(self, response):
        data = json.loads(response.body)
        item = PublicPrivateLawsItem()
        short_title = data.get('shortTitle')
        if short_title != None:
            title = short_title[0]['title'],
            title = title[0]
        else:
            title = data.get('title')

        item = {
            'date_issued': data.get('dateIssued'),
            'gov_info_references': data.get('references'),
            'document_type': data.get('documentType'),
            'congress': data.get('congress'),
            'document_number': data.get('documentNumber'),
            'package_id': data.get('packageId'),
            'collection_code': data.get('collectionCode'),
            'url': data.get('detailsLink'),
            'title': title,
            'long_title': data.get('title'),
            'branch': data.get('branch'),
            'collection_name': data.get('collectionName'),
            'download': data.get('download'),
            'pages': data.get('pages'),
            'government_author1': data.get('governmentAuthor1'),
            'government_author2': data.get('governmentAuthor2'),
            'su_doc_class_number' : data.get('suDocClassNumber'),
            'related_url': data.get('relatedLink'),
            'publisher': data.get('publisher'),
            'doc_class': data.get('docClass'),
            'created_at': data.get('lastModified'),
            'category': data.get('category'),
            'other_identifiers': data.get('otherIdentifier')}
        yield item