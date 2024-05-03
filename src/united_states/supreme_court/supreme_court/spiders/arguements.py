import scrapy
from supreme_court.items import SupremecourtArgumentItem
from supreme_court.pipelines import ReadArticles

class ArguementsSpider(scrapy.Spider):
    name = "arguements"
    allowed_domains = ["www.supremecourt.gov"]
    start_urls = ["https://www.supremecourt.gov/oral_arguments/oral_arguments.aspx"]

    def parse(self, response):
        arugments = response.urljoin(response.css('#ctl00_ctl00_MainEditable_sidenavContent_ctl00_hypAudio').attrib['href'])
        yield response.follow(arugments, callback=self.parse_arguments)

    # def parse_each_year(self, response):
    #     years = response.xpath('//*[@id="pagemaindiv"]/div[3]/div[1]')
    #     urls_years = years.css('a')
    #     for url in urls_years:
    #         yield response.follow(response.urljoin(url.attrib['href']), callback=self.parse_arguments)
    # def parse_each_year(self, response):
    #     years = response.xpath('//*[@id="ctl00_ctl00_MainEditable_mainContent_upButtons"]/div')
    #     urls_years = years.css('a')
    #     for url in urls_years:
    #         print(url.attrib['href'])
    #         yield response.follow(response.urljoin(url.attrib['href']), callback=self.parse_arguments)

    def parse_arguments(self, response):
        main_content = response.css('#list')
        current_arguments = main_content.xpath('//*[@id="accordion"]/div[1]')

        arguments = current_arguments.xpath('//*[@id="list"]').css('tr')
        for argument in arguments:
            if len(argument.css('td ::text').getall()) >1:
                url = response.urljoin(argument.css('a').attrib['href'])
                scrapped = ReadArticles().check_val('supreme_court_opinions', url, 'url')
                if scrapped == False:
                    yield response.follow(url, callback=self.parse_argument_audio_pdf)

    def parse_argument_audio_pdf(self, response):
        table_a_url = response.xpath('//*[@id="pagemaindiv"]/div[2]/div[2]/table').css('a')
        for atag in table_a_url:
            url = response.urljoin(atag.attrib['href'])
            if url.endswith('.pdf'):
                pdf = url
            else:
                audio = url
        items = SupremecourtArgumentItem()
        items['url'] = response.url
        items['audio_url'] = audio
        items['pdf_url'] = pdf
        items['docket_number'] = response.css('#ctl00_ctl00_MainEditable_mainContent_lblDocket ::text').get()
        items['created_at'] = response.css('#ctl00_ctl00_MainEditable_mainContent_lblDate ::text').get()
        items['title'] = response.css('#ctl00_ctl00_MainEditable_mainContent_lblCaseName ::text').get()
        items['collection_name'] = 'supreme_court_arguments'
        yield items