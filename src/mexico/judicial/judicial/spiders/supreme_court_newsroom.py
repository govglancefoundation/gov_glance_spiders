import scrapy
from judicial.items import SupremeCourtNewsroomItem
from judicial.pipelines import ReadArticles

def switch_index(string: str) -> str:
    """
    This function is used to switch the index of the string
    """
    string = string.split('de')
    stripped_string = [i.rstrip().lstrip() for i in string]
    element_at_index_1 = stripped_string.pop(1)
    stripped_string.insert(0, element_at_index_1)
    created_at = ' '.join((stripped_string))
    return created_at.title()

class SupremeCourtNewsroomSpider(scrapy.Spider):
    name = "supreme_court_newsroom"
    allowed_domains = ["www.scjn.gob.mx", "www.internet2.scjn.gob.mx"]
    start_urls = ["https://www.scjn.gob.mx/multimedia/comunicados"]
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15'

    def parse(self, response):
        table = response.xpath('//*[@id="main-content"]/div/div/div/section/div[2]/div/div/div[2]/table')
        articles = table.css('tbody').css('tr')
        for article in articles:
            url = article.css('a').attrib['href']
            print(url)
            scrapped = ReadArticles().check_url('suprema_corte_de_justicia_de_la_nacion', 'url', url)
            if scrapped == False:
                yield response.follow(url, callback=self.parse_article)

    def parse_article(self, response):
        title =[i.title() for i in response.xpath('/html/body/div[5]/div[2]/p[1]//text()').extract()]
        description = response.xpath('/html/body/div[5]/div[2]/p[2]//text()').extract()
        url = response.url
        created_at = switch_index((response.xpath('/html/body/div[5]/div[1]/p[2]/strong//text()').get()).split(' a ')[1])
        location = (response.xpath('/html/body/div[5]/div[1]/p[2]/strong//text()').get()).split(' a ')[0]
        post_number = response.xpath('/html/body/div[5]/div[1]/p[1]/strong//text()').get()
        collection_name = 'Suprema Corte de Justicia de la Nación'
        item = SupremeCourtNewsroomItem()  
        item = {
            'title': title,
            'url': url,
            'created_at': created_at,
            'location': location,
            'post_number': post_number,
            'collection_name': collection_name,
            'description': description,
            'branch': 'Judicial',
            'topic': 'Noticias'
        }
        yield item