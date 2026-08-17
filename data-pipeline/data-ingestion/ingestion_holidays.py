import requests
import json
import pandas as pd
import pandas_gbq as pdq
from google.oauth2 import service_account as sa
from google.cloud import bigquery as bq

#project details
PROJECT_ID = 'project-1fe4418a-24e0-4804-a77'
DATASET_ID = 'raw_ecommerce'
TABLE_ID = 'holidays'
TABLE_NAME = f'{DATASET_ID}.{TABLE_ID}'
URL_HOLIDAYS_BASE = 'https://nagerholidays.com/api/v4/Holidays/'
SERVICE_ACCOUNT_FILE = 'service_account_credential.json' #path to service account file

#get the holidays
def get_the_holidays():
    countries_codes = ["BR", "JP", "US", "CO", "ES", "CN", "AU", "FR", "DE", "BE", "KR", "PL", "GB", "AT"] 
    
    holidays_list = []
    for country in countries_codes:
        current_url = URL_HOLIDAYS_BASE + country + '/2026'
        r = requests.get(current_url, auth=('user', 'pass'))
        holidays_list.extend(r.json())

    return holidays_list
        
if __name__=="__main__":
    
    print("Connecting to the cloud")
    credentials = sa.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    client = bq.Client(credentials=credentials, project=PROJECT_ID)
    print("Connecting was successful")

    print("Getting the list of holidays...")
    holidays_list = get_the_holidays()
    print("Holidays got successful")

    print("Loading holidays to BigQuery...")
    job = client.load_table_from_json(holidays_list, TABLE_NAME)
    print("Loading was successful")