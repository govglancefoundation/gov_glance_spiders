import scrapy
from agencies.items import AgenciesItem
from agencies.pipelines import ReadArticles

class EntitiesSpider(scrapy.Spider):
    name = "entities"
    allowed_domains = ["www.gob.mx"]
    start_urls = ["https://www.gob.mx/gobierno"]

    def parse(self, response):
        '''
        Get the title of the agency and the url so the spider can crawl to next page
        '''
        entities = response.xpath('/html/body/main/div/section[6]/div[2]')
        urls = entities.css('a')
        for url in urls:
            if str(url.attrib['href']).startswith('https://www.gob.mx/'):
                gov_link = (url.attrib['href'])+'/archivo/prensa?idiom=en'
                print(gov_link)
                yield response.follow((gov_link), callback=self.parse_agency_news) 

    def parse_agency_news(self, response):
        articles = response.css('article')
        # db_urls = []
        name = response.xpath('/html/body/main/div/ol/li[2]/a/text()').get()
        code = response.xpath('/html/body/main/div/div[2]/div[2]/p/span[1]/a/text()').get()
        if code is not None:
            items = AgenciesItem()
            # db_urls = []
            for article in articles:    
                url = response.urljoin(article.css('a').attrib['href'])
                print(url)
                scrapped = ReadArticles().check_item(code, url)
                if scrapped == False:
                    items['url'] = response.urljoin(url)
                    items['image'] = article.css('img').attrib['src']
                    items['created_at'] = article.css('time').attrib['datetime']
                    items['type'] = article.css('p').css('span.tag-presses ::text').get()
                    items['title'] = str(article.css('h2 ::text').get())
                    items['collection_name'] = name
                    items['code'] = code
                    print(items)
                    yield items

