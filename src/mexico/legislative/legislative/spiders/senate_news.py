import scrapy
from legislative.pipelines import ReadArticles
from legislative.items import SenateNewsroomItem

class SenateNewsSpider(scrapy.Spider):
    name = "senate_news"
    allowed_domains = ["comunicacionsocial.senado.gob.mx"]
    start_urls = ["https://comunicacionsocial.senado.gob.mx/informacion/comunicados"]

    def parse(self, response):
        articles = response.css('div.items-row')
        for article in articles:
            url = response.urljoin(article.css('a').attrib['href'])
            scrapped = ReadArticles().check_url('senado_de_la_republica', 'url', url)
            if scrapped == False:
                items = SenateNewsroomItem()

                title = (article.css('a ::text').get())
                url = (url)
                created_at = (article.css('time').attrib['datetime'])
                image = response.urljoin(article.css('img').attrib['src'])
                description = (article.css('p ::text').get())
                collection_name = 'Senado De La República'
                topic = 'Noticies'
                branch = 'Legislativo'

                items = {
                    'title': title,
                    'url': url,
                    'created_at': created_at,
                    'image': image,
                    'description': description,
                    'collection_name': collection_name,
                    'topic': topic,
                    'branch': branch
                }
                yield items
        # pagination = response.xpath('//*[@id="g-main"]/div[2]/div/div/div/div/div/div[12]')
        # next_page = pagination.xpath('//*[@id="g-main"]/div[2]/div/div/div/div/div/div[12]/ul/li[13]/a/@href').extract()
        # if next_page:
        #     next_url = response.urljoin(next_page[0])
        #     print(next_url)
        #     yield response.follow(next_url, callback=self.parse)
