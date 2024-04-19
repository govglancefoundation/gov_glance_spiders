import scrapy

from executive.pipelines import ReadArticles
from executive.items import ExecutiveItemDOI

class InteriorSpider(scrapy.Spider):
    name = "interior"
    allowed_domains = ["www.doi.gov"]
    start_urls = ["https://www.doi.gov/news"]

    def parse(self, response):
        
        content = response.xpath('//*[@id="block-doi-uswds-content"]/article/div/div')
        articles = content.css('article')

        for article in articles:
            url = response.urljoin(article.css('a').attrib['href'])
            scrapped = ReadArticles().check_val('department_of_interior_news', url, 'url')
            if scrapped == False:
                item = ExecutiveItemDOI()
                item = {
                "url" : url,
                "img" : response.urljoin((article.css('img').attrib['src'])),
                "title" : (article.css('h3').css('span ::text').get()),
                "created_at" : (article.css('div.publication-info--date ::text').get()),
                "description" : (article.css('p ::text').get()),
                "collection_name" : "Department of Interior News",
                "table_name" : "department_of_interior_news"
                }
                yield item
        # if response.xpath('//*[@id="block-doi-uswds-content"]/article/div/div/div/nav/ul/li[7]/a').attrib['href']:
        #     next_url = response.urljoin(response.xpath('//*[@id="block-doi-uswds-content"]/article/div/div/div/nav/ul/li[7]/a').attrib['href'])
        #     yield response.follow(next_url, callback=self.parse)
        