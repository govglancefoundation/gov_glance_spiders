# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from psycopg2 import errors
import dateutil.parser
from scrapy.utils.project import get_project_settings


class OurcommonsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## stip the white space from titles
        field_names = adapter.field_names()

        for field_name in field_names:
            value = adapter.get(field_name)
            if value != None:
                if field_name == 'url':
                    value = adapter.get(field_name)
                    adapter[field_name] = value
                if field_name == 'collection_name':
                    value = adapter.get(field_name)
                    adapter['collection_name'] = value
                if field_name == 'title':
                    value = adapter.get(field_name)
                    items = value.split('(', 1)
                    adapter[field_name] = items[0].rstrip().lstrip() + ' Meeting'
                if field_name == 'created_at':
                    value = adapter.get(field_name)
                    # get the date
                    if type(value) is list:
                        duration = [x.rstrip().lstrip() for x in value]
                        duration.remove(',')
                        # create new list with just the hours
                        hours = duration[1].split(' to ')
                        created_at = duration[0]
                        started_at = created_at + ' ' +hours[0] 
                        ended_at = created_at + ' ' +hours[1]
                        adapter['start_at'] = str(dateutil.parser.parse(started_at))
                        adapter['end_at'] = str(dateutil.parser.parse(ended_at))
                        adapter[field_name] = str(dateutil.parser.parse(created_at))
                    if type(value) is str:
                        adapter[field_name] = str(dateutil.parser.parse(value))
                    # adapter[field_name] = str(dateutil.parser.parse(value))
                if field_name == 'parliment':
                    value = adapter.get(field_name)
                    split = value.split(',',1)
                    adapter[field_name] = split[0]
                    adapter['session'] = split[1].rstrip().lstrip()
                if field_name == 'stream_url':
                    value = adapter.get(field_name)
                    adapter[field_name] = 'https:' + value
                if field_name == 'address':
                    value = adapter.get(field_name)
                    full_address = [x.replace("\r\n"," ").rstrip().lstrip() for x in value]
                    addy = list(filter(None, full_address))
                    adapter[field_name] = ' '.join(addy)
                if field_name == 'details_link':
                    adapter[field_name] = 'https:'+adapter.get(field_name)

        return item
      
class ReadArticles:

    def __init__(self):
            
            POSTGRES_USERNAME = get_project_settings().get('POSTGRES_USERNAME')
            POSTGRES_PASS = get_project_settings().get('POSTGRES_PASSWORD')
            POSTGRES_ADDRESS = get_project_settings().get('POSTGRES_ADDRESS')
            POSTGRES_PORT = get_project_settings().get('POSTGRES_PORT')
            POSTGRES_DBNAME = get_project_settings().get('POSTGRES_DBNAME')
            self.schema = "canada"
            self.connection = psycopg2.connect(host=POSTGRES_ADDRESS, user=POSTGRES_USERNAME, password=POSTGRES_PASS, dbname=POSTGRES_DBNAME, port=POSTGRES_PORT)
            self.cur = self.connection.cursor()
    
    def check_item(self,name, url): # the name variable is something that you write in the code block
        table = name.lower().replace(' ', '_').replace("'", '').replace('-','_').replace(',','')
        topic = 'legisltive'
        print(table)
        print(url)
        try:
            self.cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.schema}.{table}(
                        id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ), 
                        url character varying(500) COLLATE pg_catalog."default",
                        title text COLLATE pg_catalog."default",
                        parliment character varying(20) COLLATE pg_catalog."default",
                        meeting_num character varying(20) COLLATE pg_catalog."default",
                        address character varying(300) COLLATE pg_catalog."default",
                        address_url character varying(500) COLLATE pg_catalog."default",
                        stream_url character varying(500) COLLATE pg_catalog."default",
                        home_url character varying COLLATE pg_catalog."default",
                        created_at timestamp with time zone,
                        start_at timestamp with time zone,
                        end_at timestamp with time zone,
                        type character varying COLLATE pg_catalog."default",
                        session character varying(20) COLLATE pg_catalog."default",
                        collection_name character varying COLLATE pg_catalog."default",
                        code character varying(20) COLLATE pg_catalog."default",
                        topic character varying COLLATE pg_catalog."default" DEFAULT '{topic}'::character varying,
                        description text,
                        collected_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT {table}_pkey PRIMARY KEY (id)
                        )
                    """)
            

            self.cur.execute(f"""SELECT url FROM {self.schema}.{table} WHERE url = '{url}'""")
            results = self.cur.fetchone()
            if results:
                print('******URL EXISTS******')
                return True
            else:
                print('******URL DOES NOT EXIST******')
                return False
        except psycopg2.Error as e:
            print(e)
            self.connection.rollback()
            raise SystemExit(-1)
        
    def check_id(self, name, bill_id):
        table = name.lower().replace(' ', '_').replace("'", '')
        self.cur.execute(f"""SELECT bio_guid_id FROM {self.schema}.{table} WHERE bio_guid_id = '{bill_id}'""")
        results = [i[0] for i in self.cur.fetchall()]
        print(results)
        if results:
            return True
        else:
            return False


class WriteOurcommonsPipeline:

    def __init__(self, POSTGRES_PASS, POSTGRES_USERNAME, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_DBNAME):
            POSTGRES_USERNAME = POSTGRES_USERNAME
            self.POSTGRES_PASS = POSTGRES_PASS
            POSTGRES_ADDRESS = POSTGRES_ADDRESS
            POSTGRES_PORT = POSTGRES_PORT
            POSTGRES_DBNAME = POSTGRES_DBNAME
            self.schema = "canada"
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
        print(item)
        table_name = item['code'].lower().replace(' ', '_').replace("'", '').replace('-','_').replace(',','')
        schema = self.schema
        topic = 'legisltive'
        try:

            """
            - Here we can add description if we do not have it in the key of items
            - We added a condition to look for created_at to add it as a timestamp with timezone for consistency 
            - 

            """
            # columns.append("id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 )")

            # if 'description' not in item.keys():
            #     columns.append("description VARCHAR")
            
            # for key in item.keys():
            #     if key == 'created_at':
            #         columns.append(f'{key} timestamp with time zone')
            #     elif key in ['depication', 'terms']:
            #         columns.append(f"{key} JSONB")
            #     else:
            #         columns.append(f"{key} VARCHAR")

            # # columns = [f"{key} VARCHAR" for key in item.keys()] # removed this code and made it so it looks for craeted at 
            
            # '''
            # These appends are gor the columns that every table will need like id, topic, and collected_at
            # '''
            # columns.append(f"""topic character varying COLLATE pg_catalog."default" DEFAULT '{topic}'::character varying""")
            # columns.append(f"""CONSTRAINT {table_name}_pkey PRIMARY KEY (id)""")
            # columns.append("collected_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP")

            # # Constructing the full query
            # query = f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} ({', '.join(columns)})"
            # self.cur.execute(query)
            self.cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.schema}.{table_name}(
                        id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ), 
                        url character varying(500) COLLATE pg_catalog."default",
                        title text COLLATE pg_catalog."default",
                        parliment character varying(20) COLLATE pg_catalog."default",
                        meeting_num character varying(20) COLLATE pg_catalog."default",
                        address character varying(300) COLLATE pg_catalog."default",
                        address_url character varying(500) COLLATE pg_catalog."default",
                        stream_url character varying(500) COLLATE pg_catalog."default",
                        home_url character varying COLLATE pg_catalog."default",
                        created_at timestamp with time zone,
                        start_at timestamp with time zone,
                        end_at timestamp with time zone,
                        type character varying COLLATE pg_catalog."default",
                        session character varying(20) COLLATE pg_catalog."default",
                        collection_name character varying COLLATE pg_catalog."default",
                        code character varying(20) COLLATE pg_catalog."default",
                        topic character varying COLLATE pg_catalog."default" DEFAULT '{topic}'::character varying,
                        description text,
                        collected_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT {table_name}_pkey PRIMARY KEY (id)
                        )
                    """)
            
            if item:
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