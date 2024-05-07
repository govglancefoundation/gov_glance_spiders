import json
import scrapy
from scrapy.utils.project import get_project_settings

COURT_LISTENER_API_KEY = get_project_settings().get('COURT_LISTENER_API_KEY')

class OpinionsSpider(scrapy.Spider):
    name = "opinions"
    allowed_domains = ["www.courtlistener.com"]
    start_urls = ["https://www.courtlistener.com/api/rest/v3/opinions/?cluster__docket__court__id=", "https://www.courtlistener.com/api/rest/v3/dockets/?court__id="]
    headers = {"Authorization": f"Token {COURT_LISTENER_API_KEY}"}

    def parse(self, response):
        abbrev = ["ala","alaska","ariz","ark","cal","colo","conn","del","fla","ga","haw","idaho","ill","ind","iowa","kan","ky","la","mich","minn","miss","mo","mont","neb","nev","nh","nj","nm","nc","nd","ohio","okla","or","pa","ri","sc","sd","tenn","tex","utah","vt","va","wash","wva","wis","wyo"][:1]
        
        for state in abbrev:
            yield response.follow(f"https://www.courtlistener.com/api/rest/v3/opinions/?cluster__docket__court__id={state}", callback=self.parse_dockets, headers=self.headers)
    
    def parse_article(self, response):
        return None