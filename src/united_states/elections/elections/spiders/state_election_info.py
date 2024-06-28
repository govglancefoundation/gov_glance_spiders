import scrapy
import re

class StateElectionInfoSpider(scrapy.Spider):
    name = "state_election_info"
    allowed_domains = ["www.eac.gov"]
    start_urls = ["https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18156","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18161","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18166","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18171","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18176","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18181","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18186","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18191","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18196","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18201","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18206","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18211","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18216","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18221","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18226","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18231","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18236","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18241","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18246","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18251","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18256","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18261","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18266","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18271","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18276","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18281","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18286","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18291","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18296","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18301","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18306","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18311","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18316","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18321","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18326","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18331","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18336","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18341","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18346","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18351","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18356","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18361","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18366","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18371","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18376","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18381","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18386","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18391","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18396","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18401","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18406""https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18426","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18431","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18436","https://www.eac.gov/voters/register-and-vote-in-your-state?field_state_target_id=18441"]

    def parse(self, response):
        content = response.css('div.content-news-page')

        # state name
        state_name = content.css('h3 ::text').get()
        print(state_name)

        # Any numbers for the election page
        phone_numbers = [tag.get() for tag in content.css('p ::text')]

        # this is for the table of elections and their deadlines
        rows  = content.css('table')[0].css('tr')[1:]
        info_tables = {}
        for row in rows:
            items = row.css('td ::text').getall()
            key = items[0].lstrip().rstrip()
            values = []
            for val in items[1:]:
                if 'Election Dates' in val:
                    pass
                if 'Registration Deadlines' in val:
                    pass
                else:
                    val = val.rstrip().lstrip()
                    values.append(val)
            info_tables[key] = values

        # for row in table_rows[1:]:
        #     item = row.css('td ::text').getall()
        #     table_data[item[0]] = item[1]

        # Resources for elections - title and url
        urls = content.css('a')
        urls_dict = {}
        for url in urls:
            if url.css('a::attr(title)').get():
                title = url.css('a::attr(title)').get()
                url = url.css('a').attrib['href']
                urls_dict[title] = url
        

        em_tags = content.css('em ::text')
        for tag in em_tags:
            string = tag.get()
            if 'Updated on' in string:
                date = string

        yield {
            'state': state_name,
            'eac_url': response.url,
            'phone_numbers': phone_numbers, # will be cleaned in the pipelines.py
            'polling_info_urls': urls_dict,
            'election_info': info_tables,
            'updated_at': date, # will be cleaned in the pipelines.py
            'collection_name': 'state_election_info'
        }