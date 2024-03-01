import scrapy
from scrapy.exceptions import CloseSpider
import json
from congressional.pipelines import ReadArticles
from congressional.items import CongressionalMembersItem
from scrapy.utils.project import get_project_settings

CONGRESS_API_KEY = get_project_settings().get('CONGRESS_API_KEY')
#21 json lines
class MembersSpider(scrapy.Spider):
    name = "members"
    allowed_domains = ["api.congress.gov"]
    start_urls = [f"https://api.congress.gov/v3/member?format=json&limit=250&api_key={CONGRESS_API_KEY}"]
   

    def parse(self, response):
        data = json.loads(response.body)
        for member in data['members']:
            item = CongressionalMembersItem()
            scrapped = ReadArticles().check_id('members', member.get('bioguideId'))
            if scrapped == False:

                item = {
                    'bio_guid_id': member.get('bioguideId'),
                    'depication': member.get('depiction'),
                    'district': member.get('district'),
                    'name': member.get('name'),
                    'party_name': member.get('partyName'),
                    'state': member.get('state'),
                    'terms': member.get('terms'),
                    'created_at': member.get('updateDate'),
                    'url': member.get('url'),
                    'collection_name': 'Members',
                }
                yield item

        if 'next' in data['pagination']:

            yield response.follow(data['pagination']['next']+f'&api_key={CONGRESS_API_KEY}', self.parse)