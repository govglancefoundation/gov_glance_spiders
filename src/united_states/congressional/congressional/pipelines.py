# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import json
import dateutil.parser
from scrapy.utils.project import get_project_settings

class CongressionalPipeline:
    def process_item(self, item, spider):
        bill_id = None

        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
  
        if adapter['collection_name'] in ['Congressional Hearings', 'Public and Private Laws']:
            field1_value = adapter['document_type']
            cham = field1_value.split('HR')[0]
            if cham == 'H':
                full_title = adapter['title'].title()

            else:
                field2_value = adapter['congress']
                field3_value = adapter['document_number']
                title = adapter['title'].title()
                full_title = f"{cham}. Hrg. {field2_value}-{field3_value} - {title}"
            adapter['status_title'] = full_title
        if adapter['collection_name'] in ['Congressional Bills', 'Congressional Bills Enrolled']:
            field1_value = adapter['bill_type'].upper()
            field2_value = adapter['bill_number']
            field3_value = adapter['bill_version'].upper()
            field4_value = adapter['title']
            full_title = f"{field1_value}. {field2_value} ({field3_value}) - {field4_value}"
            adapter['status_title'] = full_title
        
        for field_name in field_names:
            if field_name == 'package_id':
                bill_id = adapter[field_name]
        for field_name in field_names:
            value = adapter[field_name]
            if value is not None:
                if field_name == 'download':
                    download_urls =adapter[field_name]
                    for key, value in download_urls.items():
                        if key in ['modsLink', 'premisLink']:
                            url_string = value
                            url_extention = url_string.split('/')[-1]
                            download_url = url_string.replace("api","www").replace("/packages/", "/metadata/pkg/").replace(url_extention, '') +f'{url_extention}.xml'
                            download_urls[key] = download_url

                        if key == 'xmlLink':
                            url_string = value
                            url_extention = url_string.split('/')[-1]
                            download_url = url_string.replace("api","www").replace("/packages/", "/content/pkg/")+f'/{bill_id}.xml'
                            download_urls[key] = download_url
                        if key == 'txtLink':
                            url_string = value
                            url_extention = url_string.split('/')[-1]
                            download_url = url_string.replace("api","www").replace("/packages/", "/content/pkg/")+f'l/{bill_id}.{url_extention}'
                            download_urls[key] = download_url
                        if key == 'zipLink':
                            url_string = value
                            url_extention = url_string.split('/')[-1]
                            download_url = url_string.replace("api","www").replace("/packages/", "/content/pkg/").replace(f"/{url_extention}","")+f'.{url_extention}'
                            download_urls[key] = download_url
                        if key == 'pdfLink':
                            url_string = value
                            url_extention = url_string.split('/')[-1]
                            download_url = url_string.replace("api","www").replace("/packages/", "/content/pkg/")+f'/{bill_id}.{url_extention}'
                            download_urls[key] = download_url
                    adapter[field_name] = download_urls
                if field_name in ['long_title', 'title']:
                    value = adapter[field_name].title()
                    adapter[field_name] = value
                if field_name == 'created_at':
                    value = adapter[field_name]
                    adapter[field_name] = dateutil.parser.parse(value)
                if field_name in ['download', 'related', 'other_identifiers', 'topics', 'committees', 'members', 'held_dates', 'serial_set', 'subjects', 'gov_info_references']:
                    value = adapter[field_name]
                    adapter[field_name] = json.dumps(value)

        return item

class ReadArticles:

    def __init__(self):
            
            POSTGRES_USERNAME = get_project_settings().get('POSTGRES_USERNAME')
            POSTGRES_PASS = get_project_settings().get('POSTGRES_PASSWORD')
            POSTGRES_ADDRESS = get_project_settings().get('POSTGRES_ADDRESS')
            POSTGRES_PORT = get_project_settings().get('POSTGRES_PORT')
            POSTGRES_DBNAME = get_project_settings().get('POSTGRES_DBNAME')
            self.schema = "united_states_of_america"
            self.connection = psycopg2.connect(host=POSTGRES_ADDRESS, user=POSTGRES_USERNAME, password=POSTGRES_PASS, dbname=POSTGRES_DBNAME, port=POSTGRES_PORT)
            self.cur = self.connection.cursor()
    
    def check_item(self,name, bill_id, modified_date): # the name variable is something that you write in the code block
        
        table = name.lower()
        self.cur.execute(f"""SELECT package_id, created_at FROM {self.schema}.{table} WHERE package_id = '{bill_id}' AND created_at = '{modified_date}'""")
        results = [i[0] for i in self.cur.fetchall()]
        print(results)
        if results:
            return True
        else:
            return False


class WriteCongressionalBills:

    def __init__(self, POSTGRES_PASS, POSTGRES_USERNAME, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_DBNAME):
            POSTGRES_USERNAME = get_project_settings().get('POSTGRES_USERNAME')
            POSTGRES_PASS = get_project_settings().get('POSTGRES_PASSWORD')
            POSTGRES_ADDRESS = get_project_settings().get('POSTGRES_ADDRESS')
            POSTGRES_PORT = get_project_settings().get('POSTGRES_PORT')
            POSTGRES_DBNAME = get_project_settings().get('POSTGRES_DBNAME')
            
            self.schema = "united_states_of_america"
            self.connection = psycopg2.connect(host=POSTGRES_ADDRESS, user=POSTGRES_USERNAME, password=POSTGRES_PASS, dbname=POSTGRES_DBNAME, port=POSTGRES_PORT)
            self.cur = self.connection.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        POSTGRES_PASS = settings.get("POSTGRES_PASS")
        POSTGRES_USERNAME = settings.get("POSTGRES_USERNAME")
        POSTGRES_ADDRESS = settings.get("POSTGRES_ADDRESS")
        POSTGRES_PORT = settings.get("POSTGRES_PORT")
        POSTGRES_DBNAME = settings.get("POSTGRES_DBNAME")

        return cls(POSTGRES_PASS, POSTGRES_USERNAME, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_DBNAME)

    def process_item(self, item, spider): # Here we are going to get a dictionary or dataframe and publish new data
        try:

            table_name = item['collection_name'].lower().replace(' ', '_')
            schema = self.schema
            columns = ', '.join(item.keys())
            values = ', '.join('%({})s'.format(key) for key in item.keys())
            # values = ', '.join('%({})s'.format(key) if not 'references' else 'ARRAY[%({})s]::TEXT[]'.format(key) for key in item.keys())
            query = f"INSERT INTO {schema}.{table_name} ({columns}) VALUES ({values})"
            # print(query)
            self.cur.execute(query, item)
            self.connection.commit()
        except psycopg2.Error as e:
            print("Error: ", e)

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()