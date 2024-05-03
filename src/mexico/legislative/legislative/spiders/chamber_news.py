import scrapy
from legislative.items import ChamberOfDeputiesNewsItem
from legislative.pipelines import ReadArticles

class ChamberNewsSpider(scrapy.Spider):
    name = "chamber_news"
    allowed_domains = ["comunicacionsocial.diputados.gob.mx"]
    start_urls = ["https://comunicacionsocial.diputados.gob.mx/index.php/boletines?p=1"]
    # start_urls = ["https://comunicacionsocial.diputados.gob.mx/index.php/boletines?p=671"]
    def parse(self, response):
        collection_name = 'Chamber of Deputies'
        articles = response.css('div.col-xl-12')

        for article in articles:
            url = article.css('a').attrib['href']
            scrapped = ReadArticles().check_url('chamber_of_deputies', 'url', url)
            if scrapped == False:
                items = ChamberOfDeputiesNewsItem()
                items['url'] = url
                items['image'] = (article.css('img').attrib['src'])
                items['created_at'] = (((article.css('li ::text').getall())[-1]))
                items['title'] = (article.css('h2').css('a ::text').get())
                items['collection_name'] = collection_name
                items['branch'] = 'Legislativo'
                items['topic'] = 'Noticias'
                yield items
        
        # pagination = response.xpath('//*[@id="wrapper"]/section[2]/div/div/div[1]/div[2]/div[1]/div')
        # previous_page = response.urljoin(pagination.xpath('//a[@aria-label="Previous"]').attrib['href'])
        # if previous_page:
        #     yield response.follow(previous_page, self.parse)