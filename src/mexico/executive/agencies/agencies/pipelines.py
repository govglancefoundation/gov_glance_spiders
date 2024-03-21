# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os, sys
import psycopg2
import psycopg2.errors
import dateutil.parser
from scrapy.utils.project import get_project_settings


class AgenciesPipeline:
    def process_item(self, item, spider):
        if item is not None:
            adapter = ItemAdapter(item)
            field_names = adapter.field_names()

            for field_name in field_names:
                if field_name == 'description':
                
                    if adapter.get(field_name) != None:
                        adapter[field_name] = adapter.get(field_name)
                    else:
                        pass
                if field_name == 'code':
                    adapter['code'] = adapter.get('code').replace('/','_')
                        
            return item
        
class ReadArticles:

    def __init__(self):
            
            POSTGRES_USERNAME = get_project_settings().get('POSTGRES_USERNAME')
            POSTGRES_PASS = get_project_settings().get('POSTGRES_PASSWORD')
            POSTGRES_ADDRESS = get_project_settings().get('POSTGRES_ADDRESS')
            POSTGRES_PORT = get_project_settings().get('POSTGRES_PORT')
            POSTGRES_DBNAME = get_project_settings().get('POSTGRES_DBNAME')
            self.schema = "mexico"
            self.connection = psycopg2.connect(host=POSTGRES_ADDRESS, user=POSTGRES_USERNAME, password=POSTGRES_PASS, dbname=POSTGRES_DBNAME, port=POSTGRES_PORT)
            self.cur = self.connection.cursor()
    
    def check_item(self,name, url): # the name variable is something that you write in the code block
        table_name = name.lower().replace(' ', '_').replace("'", '').replace('-','_').replace(',','').replace('/','_')
        topic = 'executive'
        print(table_name)
        print(url)
        try:
            self.cur.execute(f"""     
                    CREATE TABLE IF NOT EXISTS {self.schema}.{table_name}(
                        id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ), 
                        url character varying(500) COLLATE pg_catalog."default",
                        title text COLLATE pg_catalog."default",
                        created_at timestamp with time zone,
                        image character varying(500) COLLATE pg_catalog."default",
                        type character varying COLLATE pg_catalog."default",
                        code character varying(20) COLLATE pg_catalog."default",
                        collection_name character varying COLLATE pg_catalog."default",
                        description text COLLATE pg_catalog."default",
                        topic character varying COLLATE pg_catalog."default" DEFAULT '{topic}'::character varying,
                        collected_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT {table_name}_pkey PRIMARY KEY (id)
                    )
                    """)
            self.connection.commit()
            self.cur.execute(f"""SELECT url FROM {self.schema}.{table_name} WHERE url = '{url}'""")
            results = self.cur.fetchone()
            if results:
                print('******URL EXISTS******')
                return True
            else:
                print('******URL DOES NOT EXIST******')
                return False
        except psycopg2.errors.UndefinedTable as e:
            print(e)
            self.connection.rollback()
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

class WriteAgenciesPipeline:

    def __init__(self):
            POSTGRES_USERNAME = get_project_settings().get('POSTGRES_USERNAME')
            POSTGRES_PASS = get_project_settings().get('POSTGRES_PASSWORD')
            POSTGRES_ADDRESS = get_project_settings().get('POSTGRES_ADDRESS')
            POSTGRES_PORT = get_project_settings().get('POSTGRES_PORT')
            POSTGRES_DBNAME = get_project_settings().get('POSTGRES_DBNAME')
            self.schema = "mexico"
            self.connection = psycopg2.connect(host=POSTGRES_ADDRESS, user=POSTGRES_USERNAME, password=POSTGRES_PASS, dbname=POSTGRES_DBNAME, port=POSTGRES_PORT)
            self.cur = self.connection.cursor()

    def process_item(self, item, spider): # Here we are going to get a dictionary or dataframe and publish new data
        print(item)
        table_name = item['code'].lower().replace(' ', '_').replace("'", '').replace('-','_').replace(',','')
        schema = self.schema
        topic = 'executive'
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
                        created_at timestamp with time zone,
                        image character varying(500) COLLATE pg_catalog."default",
                        type character varying COLLATE pg_catalog."default",
                        code character varying(20) COLLATE pg_catalog."default",
                        collection_name character varying COLLATE pg_catalog."default",
                        description text COLLATE pg_catalog."default",
                        topic character varying COLLATE pg_catalog."default" DEFAULT '{topic}'::character varying,
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
            self.connection.rollback()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
