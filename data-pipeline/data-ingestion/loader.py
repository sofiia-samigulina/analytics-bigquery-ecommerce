import requests
from google.oauth2 import service_account as sa
from google.cloud import bigquery as bq
import time

#project details
MY_PROJECT_ID = 'project-1fe4418a-24e0-4804-a77'
ECOMMERCE_DATASET_ID = 'bigquery-public-data.thelook_ecommerce'
DATASET_ID = 'raw_ecommerce'
URL_HOLIDAYS_BASE = 'https://nagerholidays.com/api/v4/Holidays/' #API without a key for access
SERVICE_ACCOUNT_FILE = 'data-pipeline/data-ingestion/service_account_credential.json' #path to service account file

#get the holidays
def get_the_holidays():
    #only countries from the dataset
    countries_codes = ["BR", "JP", "US", "CO", "ES", "CN", "AU", "FR", "DE", "BE", "KR", "PL", "GB", "AT"] 
    countries_total = len(countries_codes)

    years = ["2025", "2026"] #TODO: try calendrafic besause it has more years (from 2019)
    years_total = len(years)
    
    holidays_list = []

    for year in years:
        country_count = 0
        print(f'Getting the holidays for the year {year}...')
        for country in countries_codes:
            current_url = URL_HOLIDAYS_BASE + country + f'/{year}'
            r = requests.get(current_url, auth=('user', 'pass'))
            #TODO: add the log file
            if r.status_code != 200:
                print(f'For {country} and year {year} a response failed')
                continue
            holidays_list.extend(r.json())
            if r.status_code == 200:
                country_count += 1
        print(f'For the year {year}: {country_count} countries were successful.')
        time.sleep(1) #to avoid the API limit

    return holidays_list

def load_holidays_to_bigquery():
    holidays_list = get_the_holidays()

    job_config = bq.LoadJobConfig(
        write_disposition=bq.WriteDisposition.WRITE_TRUNCATE,
        schema = [
            bq.SchemaField("date", "DATE"),
            bq.SchemaField("name", "STRING"),
            bq.SchemaField("countryCode", "STRING"),
            bq.SchemaField("subdivisionCodes", "STRING", mode="REPEATED"),
            bq.SchemaField("nationalHoliday", "BOOLEAN"),
            bq.SchemaField("holidayTypes", "STRING", mode="REPEATED")
        ]
    )
    print("Loading holidays to BigQuery...")
    job = client.load_table_from_json(holidays_list, f'{DATASET_ID}.holidays', job_config = job_config)
    print("Loading holidays was successful")

def create_query_partitions(table_id, partition_key):
    query = f"""
        CREATE OR REPLACE TABLE `{DATASET_ID}.{table_id}`
        PARTITION BY DATE({partition_key})
        AS
        SELECT * FROM `{ECOMMERCE_DATASET_ID}.{table_id}`;
    """
    return query

def create_base_query(table_id):
    query = f"""
        CREATE OR REPLACE TABLE `{DATASET_ID}.{table_id}`
        AS
        SELECT * FROM `{ECOMMERCE_DATASET_ID}.{table_id}`;
    """
    return query

if __name__=="__main__":
    
    #1 Connecting to BigQuery
    print("Connecting to the cloud")
    credentials = sa.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    client = bq.Client(credentials=credentials, project=MY_PROJECT_ID)
    print("Connecting was successful")

    #2 Loading the holidays to BigQuery
    load_holidays_to_bigquery()

    #3 Ingesting the tables from thelook_ecommerce

    #creating partitions for tables and loading
    tables_to_partition = ['orders', 'order_items', 'events', 'inventory_items']
    for table in tables_to_partition:
        print(f"Partitioning and loading the table {table}...")
        query = create_query_partitions(table, 'created_at')
        query_job = client.query(query)
        rows = query_job.result()  # Waits for query to finish
        print(f"Partitioning and loading the table {table} was successful")

    #loading the rest of the tables without partitions
    tables_to_load = ['products', 'users', 'distribution_centers']
    for table in tables_to_load:
        print(f"Loading the table {table}...")
        query = create_base_query(table)
        query_job = client.query(query)
        rows = query_job.result()  # Waits for query to finish
        print(f"Loading the table {table} was successful")