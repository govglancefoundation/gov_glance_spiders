# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import dateutil.parser
from scrapy.utils.project import get_project_settings

class ExecutivePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name == 'created_at':
                value = adapter.get(field_name)
                adapter[field_name] = str(dateutil.parser.parse(value))
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
    
    def check_tuple(self,name,val1_name, val1, val2_name, val2): # the name variable is something that you write in the code block
        
        table = name.lower()
        self.cur.execute(f"""SELECT {val1_name}, {val2_name} FROM {self.schema}.{table} WHERE {val1_name} = '{val1}' AND {val2_name} = '{val2}'""")
        results = [i[0] for i in self.cur.fetchall()]
        print(results)
        if results:
            print(f'{val1} exists, skipping insert')
            return True
        else:
            return False
        
    def check_val(self, name, value, val_name):
        table = name.lower()
        print(value)
        self.cur.execute(f"""SELECT {val_name} FROM {self.schema}.{table} WHERE {val_name} = '{value}'""")
        results = [i[0] for i in self.cur.fetchall()]
        print(results)
        if results:
            return True
        else:
            return False
        
class WriteExecuitveArticles:

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
        topic = 'executive'
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
                if key in ['created_at', 'signing_date']:
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
            query = f"INSERT INTO {schema}.{table_name} ({columns}) VALUES ({values})"
            # print(query)
            self.cur.execute(query, item)
            print(f"Item inserted to {schema}.{table_name}")
            self.connection.commit()
        except psycopg2.Error as e:
            print("Error: ", e)

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()