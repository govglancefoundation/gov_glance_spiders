import scrapy
from representatives.pipelines import ReadArticles


class HistoricalExecutiveOrdersSpider(scrapy.Spider):
    name = "historical_executive_orders"
    allowed_domains = ["www.presidency.ucsb.edu"]
    start_urls = ["https://www.presidency.ucsb.edu/documents/app-categories/written-presidential-orders/presidential/executive-orders?page=130"]
    # start_urls = ['https://www.presidency.ucsb.edu/documents/app-categories/written-presidential-orders/presidential/executive-orders?page=698']
    # start_urls = ['https://www.presidency.ucsb.edu/documents/app-categories/written-presidential-orders/presidential/executive-orders?page=900']

    def parse(self, response):
        main_content = response.xpath('//*[@id="block-system-main"]/div/div[4]')
        articles = main_content.css('div.views-row')
        for article in articles:
            date = article.css('span.date-display-single').attrib['content']
            url = response.urljoin(article.css('div.field-title').css('a').attrib['href'])
            scrapped = ReadArticles().check_tuple('president_executive_orders','url', url, 'created_at', date)
            if scrapped == False:
                yield response.follow(response.urljoin(article.css('a').attrib['href']),callback=self.parse_article)

        if response.css('li.next'):
            next_url = response.urljoin(response.css('li.next').css('a').attrib['href'])
            print(next_url)
            yield response.follow(next_url, callback=self.parse)
            
    def parse_article(self, response):
        main_content = response.xpath('//*[@id="block-system-main"]/div/div/div[1]')
        president = main_content.css('h3').css('a ::text').get()
        title = main_content.css('div.field-ds-doc-title').css('h1 ::text').get()
        date = main_content.css('span.date-display-single').attrib['content']
        description = main_content.css('div.field-docs-content').get()
        deposition_notes = main_content.css('div.field-docs-footnote').css('p ::text').get()
        yield {
            'president': president,
            'url': response.url,
            'collection_name': 'President Executive Orders',
            'title': title,
            'created_at': date,
            'description': description,
            'disposition_notes': deposition_notes,
            'doc_type': 'Presidential Document',
            'subtype': 'Executive Order',
            'executive_order_number': None,
        }

