import scrapy


class StateOfTheUnionSpider(scrapy.Spider):
    name = "state_of_the_union"
    allowed_domains = ["www.presidency.ucsb.edu"]
    start_urls = ["https://www.presidency.ucsb.edu/documents/app-categories/spoken-addresses-and-remarks/presidential/state-the-union-addresses"]

    def parse(self, response):
        main_content = response.xpath('//*[@id="block-system-main"]/div/div[4]')
        articles = main_content.css('div.views-row')
        for article in articles:
            yield response.follow(response.urljoin(article.css('a').attrib['href']),callback=self.parse_article)
        if response.css('li.next'):
            next_url = response.urljoin(response.css('li.next').css('a').attrib['href'])
            print(next_url)
            yield response.follow(next_url, callback=self.parse)

    def parse_article(self, response):
        main_content = response.xpath('//*[@id="block-system-main"]/div/div/div[1]')
        president = main_content.css('h3').css('a ::text').get()
        title = main_content.css('div.field-ds-doc-title').css('h1 ::text').get().replace('Executive Order', '')
        date = main_content.css('span.date-display-single').attrib['content']
        description = main_content.css('div.field-docs-content').get()
        deposition_notes = main_content.css('div.field-docs-footnote').css('p ::text').get()
        video_url = main_content.css('iframe').get()
        if video_url is not None:
            video_url = "https:"+main_content.css('iframe').attrib['src']
        yield {
            'president': president,
            'url': response.url,
            'video_url': video_url,
            'collection_name': 'State of the Union Address',
            'title': title,
            'created_at': date,
            'description': description,
            'disposition_notes': deposition_notes,
            'doc_type': 'Presidential Document',
            'subtype': 'State of the Union',
        }
