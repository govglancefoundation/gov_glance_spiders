import scrapy
import json
from representatives.pipelines import ReadArticles

class PresidentExecutiveOrdersSpider(scrapy.Spider):
    name = "president_executive_orders"
    allowed_domains = ["www.federalregister.gov"]
    start_urls = [
                "https://www.federalregister.gov/api/v1/documents.json?conditions%5Bcorrection%5D=0&conditions%5Bpresident%5D=joe-biden&conditions%5Bpresidential_document_type%5D=executive_order&conditions%5Btype%5D%5B%5D=PRESDOCU&fields%5B%5D=citation&fields%5B%5D=document_number&fields%5B%5D=end_page&fields%5B%5D=html_url&fields%5B%5D=pdf_url&fields%5B%5D=type&fields%5B%5D=subtype&fields%5B%5D=publication_date&fields%5B%5D=signing_date&fields%5B%5D=start_page&fields%5B%5D=title&fields%5B%5D=disposition_notes&fields%5B%5D=executive_order_number&fields%5B%5D=not_received_for_publication&fields%5B%5D=full_text_xml_url&fields%5B%5D=body_html_url&fields%5B%5D=json_url&include_pre_1994_docs=true&maximum_per_page=10000&order=executive_order&per_page=10000",
                  ]

    def parse(self, response):
        data = json.loads(response.body)
        for item in data['results']:
            scrapped = ReadArticles().check_val('president_executive_orders', item.get('document_number'), 'document_number')
            pres = data['description']
            if scrapped == False:
                yield {
                    'citation': item.get('citation'),
                    'document_number': item.get('document_number'),
                    'end_page': item.get('end_page'),
                    'url': item.get('html_url'),
                    'pdf_url': item.get('pdf_url'),
                    'doc_type': item.get('type'),
                    'subtype': item.get('subtype'),
                    'created_at': item.get('publication_date'),
                    'signing_date': item.get('signing_date'),
                    'start_page': item.get('start_page'),
                    'title': item.get('title'),
                    'disposition_notes': item.get('disposition_notes'),
                    'executive_order_number': item.get('executive_order_number'),
                    'not_received_for_publication': item.get('not_received_for_publication'),
                    'full_text_xml_url': item.get('full_text_xml_url'),
                    'body_html_url': item.get('body_html_url'),
                    'json_url': item.get('json_url'),
                    'president': pres,
                    'collection_name': 'President Executive Orders'
                    }
        # if data.get('next_page_url'):
        #     yield response.follow(data['next_page_url'], callback=self.parse)