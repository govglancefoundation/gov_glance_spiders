import scrapy
from supreme_court.items import SupremecourtItem
from supreme_court.pipelines import ReadArticles


class OpinionsSpider(scrapy.Spider):
    name = "opinions"
    allowed_domains = ["www.supremecourt.gov"]
    start_urls = ["https://www.supremecourt.gov/opinions/opinions.aspx"]

    def parse(self, response):
        current_opinions = response.xpath('//*[@id="ctl00_ctl00_MainEditable_sidenavContent_ctl00_hypOpinion"]')
        yield response.follow(response.urljoin(current_opinions.attrib['href']), callback=self.parse_each_year)
    
    def parse_each_year(self, response):
        years = response.xpath('//*[@id="ctl00_ctl00_MainEditable_mainContent_upButtons"]/div')
        urls_years = years.css('a')
        for url in urls_years[1:-1]:
            if url.attrib['href'] != '../USReports.aspx':
                print(url.attrib['href'])
                yield response.follow(response.urljoin(url.attrib['href']), callback=self.parse_opinions)
                
        opinions = response.xpath('//*[@id="accordion"]').css('tr')
        for opinion in opinions:
            item = SupremecourtItem()
            if len(opinion.css('td ::text').getall()) >1:
                results = (opinion.css('td ::text').getall())
                url = response.urljoin(opinion.css('a').attrib['href'])
                scrapped = ReadArticles().check_val('supreme_court_opinions', url, 'url')
                if scrapped == False:
                    item['r'] = results[0]
                    item['created_at'] = results[1]
                    item['docket_number'] = results[2]
                    item['url'] = url
                    item['title'] = results[3]
                    item['justice'] = results[4]
                    item['collection_name'] = 'supreme_court_opinions'
                    yield item

    def parse_opinions(self, response):
        opinions = response.xpath('//*[@id="accordion"]').css('tr')
        for opinion in opinions:
            item = SupremecourtItem()
            if len(opinion.css('td ::text').getall()) >1:
                results = (opinion.css('td ::text').getall())
                url = response.urljoin(opinion.css('a').attrib['href'])
                scrapped = ReadArticles().check_val('supreme_court_opinions', url, 'url')
                if scrapped == False:
                    item['r'] = results[0]
                    item['created_at'] = results[1]
                    item['docket_number'] = results[2]
                    item['url'] = url
                    item['title'] = results[3]
                    item['justice'] = results[4]
                    item['collection_name'] = 'supreme_court_opinions'
                    yield item
