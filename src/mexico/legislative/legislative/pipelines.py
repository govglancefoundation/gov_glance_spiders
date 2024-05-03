# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from scrapy.utils.project import get_project_settings
import dateutil.parser
from psycopg2 import errors
import logging


def convert_abbrevs(str= 'String Date'):
    mexican_month_abbreviations = {'Ene': 'Jan','Feb': 'Feb','Mar': 'Mar','Abr': 'Apr','May': 'May','Jun': 'Jun','Jul': 'Jul','Ago': 'Aug','Sep': 'Sep','Oct': 'Oct','Nov': 'Nov','Dic': 'Dec', 'Enero': 'Jan', 'Febrero': 'Feb', 'Marzo': 'Mar', 'Abril': 'Apr', 'Mayo': 'May', 'Junio': 'Jun', 'Julio': 'Jul', 'Agosto': 'Aug', 'Septiembre': 'Sep', 'Octubre': 'Oct', 'Noviembre': 'Nov', 'Diciembre': 'Dec', 'Lunes': 'Mon', 'Martes': 'Tue', 'Miércoles': 'Wed', 'Jueves': 'Thu', 'Viernes': 'Fri', 'Sábado': 'Sat', 'Domingo': 'Sun'}
    # Split the input sentence into individual abbreviations
    mexican_abbreviations = [abbr.strip() for abbr in str.split()]

    print(mexican_abbreviations)
    # Convert each Mexican abbreviation to English, checking if it's a key in the dictionary
    for abbrev in mexican_abbreviations:
        if mexican_month_abbreviations.get(abbrev):

            abbrev = (mexican_month_abbreviations.get(abbrev))
            mexican_abbreviations[0] = abbrev
    return (' ').join(mexican_abbreviations)

class LegislativePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name == 'created_at':
                value = convert_abbrevs(adapter.get(field_name))
                adapter[field_name] = dateutil.parser.parse(value)
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
    
    def check_item(self,name, bill_id, modified_date): # the name variable is something that you write in the code block
        
        table = name.lower()
        self.cur.execute(f"""SELECT package_id, created_at FROM {self.schema}.{table} WHERE package_id = '{bill_id}' AND created_at = '{modified_date}'""")
        results = [i[0] for i in self.cur.fetchall()]
        print(results)
        if results:
            return True
        else:
            return False
    
    def check_url(self, table_name, column_name, value):
        try:
            self.cur.execute(f"""SELECT {column_name} FROM {self.schema}.{table_name} WHERE {column_name} = '{value}'""")
            results = [i[0] for i in self.cur.fetchall()]
            if results:
                logging.info(f"The url {value} exists.")
                return True
            else:
                return False
    
        except errors.UndefinedTable as e:
            # Handle the UndefinedTable exception here
            logging.info(f"The table {table_name} does not exist.")
            return False
        except Exception as e:
            logging.critical("Critical : %s", str(e))
            raise SystemExit(-1)
class WriteArticles:

    def __init__(self, POSTGRES_PASS, POSTGRES_USERNAME, POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_DBNAME):
            POSTGRES_USERNAME = POSTGRES_USERNAME
            self.POSTGRES_PASS = POSTGRES_PASS
            POSTGRES_ADDRESS = POSTGRES_ADDRESS
            POSTGRES_PORT = POSTGRES_PORT
            POSTGRES_DBNAME = POSTGRES_DBNAME
            self.schema = "mexico"
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
                else:
                    columns.append(f"{key} VARCHAR")
            columns.append(f"""CONSTRAINT {table_name}_pkey PRIMARY KEY (id)""")

            columns.append("ts tsvector GENERATED ALWAYS AS (to_tsvector('english'::regconfig, (title)::text)) STORED")
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
            # print(f"{item['package_id']} inserted to {table_name}")
            self.connection.commit()
        except psycopg2.Error as e:
            print("Error: ", e)

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()