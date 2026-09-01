import requests
from google.oauth2 import service_account as sa
from google.cloud import bigquery as bq
import time
import os
from dotenv import load_dotenv, find_dotenv
from data_pipeline.constants import (MY_PROJECT_ID, ORIGINAL_DATASET_ID, RAW_DATASET_ID, 
RAW_DATASET_NAME, URL_HOLIDAYS_BASE, SERVICE_ACCOUNT_FILE)

#get the holidays
def get_the_holidays():

    #read the API key from the .env file
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    api_key = os.environ.get('API_KEY')
    if not api_key:
        raise RuntimeError("API_KEY not found in .env")

    #only countries from the dataset
    countries_codes = ["br", "jp", "us", "co", "es", "cn", "au", "fr", "de", "be", "kr", "pl", "gb", "at"] 
    countries_total = len(countries_codes)

    #years from the dataset
    years = ["2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"] 
    years_total = len(years)
    
    holidays_list = []

    for year in years:
        country_count = 0
        print(f'Getting the holidays for the year {year}...')

        for country_code in countries_codes:
            r = requests.get(URL_HOLIDAYS_BASE, params={"api_key": api_key, "country": country_code, "year": year})
            #TODO: add the log file
            if r.status_code == 401:
                raise RuntimeError("Please check your API key for the holidays API. The request was unauthorized.")
            elif r.status_code == 429:
                raise RuntimeError("You have exceeded the API request limit. Please wait and try again later.")
            elif r.status_code != 200:
                print(f"Received an error response with code {r.status_code} for {country_code} and year {year}.")
                time.sleep(0.5) #to avoid the API limit
                continue
            else:
                row = {
                    "country_code": country_code,
                    "year": int(year),
                    "payload": r.text
                }
                holidays_list.append(row)
                country_count += 1 
            time.sleep(0.5) #to avoid the API limit

        print(f'For the year {year}: {country_count} from {countries_total} countries were successful.')

    return holidays_list

def load_holidays_to_bigquery():
    holidays_list = get_the_holidays()

    if not holidays_list:
        raise RuntimeError("No holidays fetched, aborting load.")

    job_config = bq.LoadJobConfig(
        write_disposition=bq.WriteDisposition.WRITE_TRUNCATE,
        schema = [
            bq.SchemaField("country_code", "STRING"),
            bq.SchemaField("year", "INTEGER"),
            bq.SchemaField("payload", "STRING"),
        ]
    )
    print("Loading holidays to BigQuery...")
    job = client.load_table_from_json(holidays_list, f'{RAW_DATASET_NAME}.holidays', job_config = job_config)
    print("Loading holidays was successful")

def create_query_partitions(table_id, partition_key):
    query = f"""
        CREATE OR REPLACE TABLE `{RAW_DATASET_NAME}.{table_id}`
        PARTITION BY DATE_TRUNC({partition_key}, MONTH)
        AS
        SELECT * FROM `{ORIGINAL_DATASET_ID}.{table_id}`;
    """
    return query

def create_base_query(table_id):
    query = f"""
        CREATE OR REPLACE TABLE `{RAW_DATASET_NAME}.{table_id}`
        AS
        SELECT * FROM `{ORIGINAL_DATASET_ID}.{table_id}`;
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