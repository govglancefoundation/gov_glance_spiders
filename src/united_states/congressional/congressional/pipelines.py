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
        if 'package_id' in field_names:
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

                bill_version = adapter['bill_version']
                if bill_version is None:
                    bill_version = ''

                field1_value = adapter['bill_type'].upper()
                field2_value = adapter['bill_number']
                field3_value = bill_version.upper()
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
        if 'bio_guide_id' in field_names:
            for field_name in field_names:
                if field_name == 'created_at':
                    value = adapter[field_name]
                    adapter[field_name] = dateutil.parser.parse(value)
                if field_name in ['terms', 'depication', 'address_information', 'cosponsered_legislation','party_history', 'sponsored_legislation', 'terms']:
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
    
    def check_id(self, name, bill_id):
        table = name.lower()
        self.cur.execute(f"""SELECT bio_guide_id FROM {self.schema}.{table} WHERE bio_guide_id = '{bill_id}'""")
        results = [i[0] for i in self.cur.fetchall()]
        print(results)
        if results:
            return True
        else:
            return False

    def check_batch(self, items: list, table) -> list:
        table = table.lower()
        check_data_array = ','.join([f"(CAST('{x[0]}' AS character varying), CAST('{x[1]}' AS timestamp with time zone))" for x in items])
        query = f"""SELECT *
                    FROM (VALUES {check_data_array}) AS data(package_id, created_at)
                    LEFT JOIN {self.schema}.{table} AS cb 
                    ON data.package_id = cb.package_id AND data.created_at = cb.created_at
                    WHERE cb.package_id IS NULL;
                    """
        self.cur.execute(query)
        results = [i[0] for i in self.cur.fetchall()]
        return results
    
    def check_batch(self, items: list, table) -> list:
        table = table.lower()
        check_data_array = ','.join([f"(CAST('{x[0]}' AS character varying), CAST('{x[1]}' AS timestamp with time zone))" for x in items])
        query = f"""SELECT *
                    FROM (VALUES {check_data_array}) AS data(package_id, created_at)
                    LEFT JOIN {self.schema}.{table} AS cb 
                    ON data.package_id = cb.package_id AND data.created_at = cb.created_at
                    WHERE cb.package_id IS NULL;
                    """
        self.cur.execute(query)
        results = [i[0] for i in self.cur.fetchall()]
        return results

class WriteCongressionalBills:

    def __init__(self, POSTGRES_PASS, POSTGRES_USERNAME, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_DBNAME):
            POSTGRES_USERNAME = POSTGRES_USERNAME
            self.POSTGRES_PASS = POSTGRES_PASS
            POSTGRES_ADDRESS = POSTGRES_ADDRESS
            POSTGRES_PORT = POSTGRES_PORT
            POSTGRES_DBNAME = POSTGRES_DBNAME
            self.schema = "united_states_of_america"
            self.connection = psycopg2.connect(host=POSTGRES_ADDRESS, user=POSTGRES_USERNAME, password=POSTGRES_PASS, dbname=POSTGRES_DBNAME, port=POSTGRES_PORT)
            self.cur = self.connection.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        POSTGRES_USERNAME = get_project_settings().get('POSTGRES_USERNAME')
        POSTGRES_PASS = get_project_settings().get('POSTGRES_PASSWORD')
        POSTGRES_ADDRESS = get_project_settings().get('POSTGRES_ADDRESS')
        POSTGRES_PORT = get_project_settings().get('POSTGRES_PORT')
        POSTGRES_DBNAME = get_project_settings().get('POSTGRES_DBNAME')

        return cls(POSTGRES_PASS, POSTGRES_USERNAME, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_DBNAME)

    def process_item(self, item, spider): # Here we are going to get a dictionary or dataframe and publish new data
        table_name = item['collection_name'].lower().replace(' ', '_')
        schema = self.schema
        topic = 'legisltive'
        try:
            columns = []

            """
            - Here we can add description if we do not have it in the key of items
            - We added a condition to look for created_at to add it as a timestamp with timezone for consistency 
            - 

            """
            columns.append("id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 )")

            if 'description' not in item.keys():
                columns.append("description VARCHAR")
            
            for key in item.keys():
                if key == 'created_at':
                    columns.append(f'{key} timestamp with time zone')
                elif key in ['depication', 'terms', 'address_information', 'cosponsered_legislation','party_history', 'sponsored_legislation']:
                    columns.append(f"{key} JSONB")
                else:
                    columns.append(f"{key} VARCHAR")

            # columns = [f"{key} VARCHAR" for key in item.keys()] # removed this code and made it so it looks for craeted at 
            
            '''
            These appends are gor the columns that every table will need like id, topic, and collected_at
            '''
            columns.append(f"""topic character varying COLLATE pg_catalog."default" DEFAULT '{topic}'::character varying""")
            columns.append(f"""CONSTRAINT {table_name}_pkey PRIMARY KEY (id)""")
            columns.append("collected_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP")


            # Constructing the full query
            query = f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} ({', '.join(columns)})"
            self.cur.execute(query)

            
            columns = ', '.join(item.keys())
            values = ', '.join('%({})s'.format(key) for key in item.keys())
            # values = ', '.join('%({})s'.format(key) if not 'references' else 'ARRAY[%({})s]::TEXT[]'.format(key) for key in item.keys())

            query = f"INSERT INTO {schema}.{table_name} ({columns}) VALUES ({values}) RETURNING id;"
            self.cur.execute(query, item)

            id_of_new_row = self.cur.fetchone()[0]
            print(f"id for inserted item {id_of_new_row}")
            query = f"INSERT INTO world_search_results (id, source, schema_source, ts) VALUES (%s, %s, %s, to_tsvector('english'::regconfig, %s));"
            self.cur.execute(query, (id_of_new_row, table_name, schema, item['title'] ))
            # print(query)
            # print(f"{item['package_id']} inserted to {table_name}")
            self.connection.commit()
        except psycopg2.Error as e:
            print("Error: ", e)

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()