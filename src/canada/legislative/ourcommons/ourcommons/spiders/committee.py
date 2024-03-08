import scrapy
import re
from ourcommons.items import CommitteesItem
from ourcommons.pipelines import ReadArticles


class CommitteeSpider(scrapy.Spider):
    name = "committee"
    allowed_domains = ["www.ourcommons.ca"]
    start_urls = ["https://www.ourcommons.ca/Committees/en/ContactUs"]

    def parse(self, response):
        committee_list = response.css('div.committees-list-items')
        
        for item in committee_list.css('div.accordion-item'):
            urls = (item.css('div.accordion-content').css('a ::text').getall())
            collection_name = item.css('span.committee-name ::text').get() + ' Committee'
            for url in urls:
                search_ = re.search("ourcommon..ca/(.*)", url)
                if search_ is not None:
                    link = 'https://www.'+search_.group()
                    print(link)
                    yield response.follow(link, callback=self.parse_home_page, meta={'url':url, 'collection_name':collection_name})
            

    def parse_home_page(self, response):
        # meta info
        home_url = response.meta.get('url')
        collection_name = response.meta.get('collection_name')
        # response info
        meetings = response.xpath('//*[@id="meeting-accordion"]')
        committee_code = response.xpath('/html/body/div[3]/nav[1]/div/div/div/div[1]/a[2]//text()').get().lower()
        meeting_content = meetings.css('div.accordion-content')

        """
        the spider will iterate through the list of meeting urls that we do not have in the database table
        """
        for item in meeting_content:

            info = CommitteesItem()
            urls = item.css('a')
            notice_of_meeting_url = response.urljoin(urls[-1].attrib['href'])
            scrapped = ReadArticles().check_item(committee_code, notice_of_meeting_url)
            if scrapped == False:
                print(notice_of_meeting_url)
                info['url'] = notice_of_meeting_url
                info['code'] = committee_code
                info['collection_name'] = collection_name
                info['home_url'] = home_url
                yield response.follow(notice_of_meeting_url, callback=self.parse_meeting, meta={'url':info['url'], 'code':info['code'], 'collection_name':info['collection_name'], 'home_url':info['home_url']})


        news_url = response.xpath('//*[@id="collapsible-profile-navbar"]/div[1]/ul/li[6]/a/@href').get()
        yield response.follow(news_url, callback=self.parse_news_release, meta={'code':committee_code, 'collection_name':collection_name, 'home_url':home_url})

    def parse_news_release(self, response):
        # get the type of item --- this case its a news release which will be saved as a value in the items class
        info = CommitteesItem()
        item_type = 'News Release'
        # get the code to store item in to the database


        articles = response.css('a.list-group-linked-item')
        parliment = response.xpath('//*[@id="session-bold"]/text()').get()
        committee_code = response.meta.get('code')
        home_url = response.meta.get('home_url')
        collection_name = response.meta.get('collection_name')
        #find the articles for each committee
        # db_urls = []
        for article in articles:
            url = response.urljoin(article.attrib['href'])
            scrapped = ReadArticles().check_item(committee_code, url)
            if scrapped == False:
                info['title'] = article.css('span.press-release-title ::text').get()
                info['parliment'] = parliment
                info['created_at'] = article.css('span.press-release-date ::text').get()
                info['type'] = item_type
                info['code'] = committee_code
                info['url'] = url
                info['collection_name'] = collection_name
                info['home_url'] = home_url
                yield info

    def parse_meeting(self, response):
        details_link = response.meta.get('url')
        committee_code = response.meta.get('code')
        home_url = response.meta.get('home_url')
        collection_name = response.meta.get('collection_name')
        info = CommitteesItem()
        item_type = 'Committee Meeting'
        title = response.css('div.CommitteeName ::text').get()
        parliment = response.xpath('//*[@id="publicationContent"]/div/div/section/div[2]/div[3]/div/div[1]/div/main/div/div/div[2]/div[1]/text()').get()
        if parliment == None:
            parliment = response.xpath('//*[@id="publicationContent"]/div/div/section/div[2]/div[3]/div/div/div/main/div/div[1]/div[2]/div[2]/text()').get()
        meeting_num = response.css('div.MeetingNumber ::text').get()
        address = response.xpath('//*[@id="publicationContent"]/div/div/section/div[2]/div[3]/div/div[1]/div/main/div/div/div[2]/div[5]//text()').getall()
        google_address_url = response.xpath('//*[@id="publicationContent"]/div/div/section/div[2]/div[3]/div/div[1]/div/main/div/div/div[2]/div[5]//a/@href').get().replace('\n', ' ').replace('\r', '')
        # we will need to edit this when we process the data in the pipline
        stream_url =  response.xpath('//*[@id="publicationContent"]/div/div/section/div[1]/div[3]/div[2]/div[2]/div//a/@href').get()
        time = response.xpath('//*[@id="publicationContent"]/div/div/section/div[2]/div[3]/div/div[1]/div/main/div/div/div[2]/div[4]//text()').getall()
        
        info['title'] = title
        info['parliment'] = parliment
        info['created_at'] = time
        info['type'] = item_type
        info['code'] = committee_code
        info['url'] = details_link
        info['meeting_num'] = meeting_num
        info['address'] = address
        info['address_url'] = google_address_url
        info['stream_url'] = stream_url
        info['collection_name'] = collection_name
        info['home_url'] = home_url
    
        '''
        Code down below will be added to the pipline script to process the data
        '''
        yield info