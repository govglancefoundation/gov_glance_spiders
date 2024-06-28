import scrapy
from scrapy.utils.project import get_project_settings
import json
from elections.pipelines import ReadArticles

API_KEY_FEC = get_project_settings().get('API_KEY_FEC')

class SenateSpider(scrapy.Spider):
    name = "senate"
    allowed_domains = ["api.open.fec.gov"]
    start_urls = [f"https://api.open.fec.gov/v1/candidates/?page=1&per_page=100&is_active_candidate=true&election_year=2024&office=S&candidate_status=C&sort=name&sort_hide_null=false&sort_null_only=false&sort_nulls_last=false&api_key={API_KEY_FEC}"]

    def parse(self, response):
        data = json.loads(response.body)
        for item in data['results']:
            scrapped = ReadArticles().check_val('senate_candidates', item['candidate_id'], 'candidate_id' )
            if scrapped is False:
                yield { 
                    'active_through' : item["active_through"] ,
                    'candidate_id' : item["candidate_id"] ,
                    'candidate_inactive' : item["candidate_inactive"] ,
                    'candidate_status' : item["candidate_status"] ,
                    'cycles' : item["cycles"] ,
                    'district' : item["district"] ,
                    'district_number' : item["district_number"] ,
                    'election_districts' : item["election_districts"] ,
                    'election_years' : item["election_years"] ,
                    'federal_funds_flag' : item["federal_funds_flag"] ,
                    'first_file_date' : item["first_file_date"] ,
                    'has_raised_funds' : item["has_raised_funds"] ,
                    'inactive_election_years' : item["inactive_election_years"] ,
                    'incumbent_challenge' : item["incumbent_challenge"] ,
                    'incumbent_challenge_full' : item["incumbent_challenge_full"] ,
                    'last_f2_date' : item["last_f2_date"] ,
                    'last_file_date' : item["last_file_date"] ,
                    'load_date' : item["load_date"] ,
                    'name' : item["name"] ,
                    'office' : item["office"] ,
                    'office_full' : item["office_full"] ,
                    'party' : item["party"] ,
                    'party_full' : item["party_full"] ,
                    'state' : item["state"],
                    'collection_name': 'senate_candidates'
                }
            pagination = data.get('pagination')
            if pagination:
                if pagination['page'] < pagination['pages']:
                    current_page = pagination['page']
                    current_page += 1
                    url = f"https://api.open.fec.gov/v1/candidates/?page={current_page}&per_page=100&is_active_candidate=true&election_year=2024&office=S&candidate_status=C&sort=name&sort_hide_null=false&sort_null_only=false&sort_nulls_last=false&api_key={API_KEY_FEC}"
                    yield response.follow(url, callback = self.parse)
