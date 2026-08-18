import requests
from google.oauth2 import service_account as sa
from google.cloud import bigquery as bq

#project details
PROJECT_ID = 'project-1fe4418a-24e0-4804-a77'
DATASET_ID = 'raw_ecommerce'
TABLE_ID = 'holidays'
TABLE_NAME = f'{DATASET_ID}.{TABLE_ID}'
URL_HOLIDAYS_BASE = 'https://nagerholidays.com/api/v4/Holidays/' #API without a key for access
SERVICE_ACCOUNT_FILE = 'data-pipeline/data-ingestion/service_account_credential.json' #path to service account file

#get the holidays
def get_the_holidays():
    #only countries from the dataset
    countries_codes = ["BR", "JP", "US", "CO", "ES", "CN", "AU", "FR", "DE", "BE", "KR", "PL", "GB", "AT"] 
    
    holidays_list = []
    countries_count = 0
    for country in countries_codes:
        current_url = URL_HOLIDAYS_BASE + country + '/2026'
        r = requests.get(current_url, auth=('user', 'pass'))
        #TODO: add the log file
        if r.status_code != 200:
            print(f'For {country} a response failed')
            continue
        holidays_list.extend(r.json())
        countries_count += 1

    return holidays_list, countries_count

def load_holidays_to_bigquery():
    print("Getting the list of holidays...")
    holidays_list, countries_count = get_the_holidays()
    if countries_count == 14:
        print("All of the countries were successful")
    else:
        print(f"Only {countries_count} countries were successful")

    job_config = bq.LoadJobConfig(
        write_disposition=bq.WriteDisposition.WRITE_TRUNCATE,
        schema = [
            bq.SchemaField("date", "DATE"),
            bq.SchemaField("name", "STRING"),
            bq.SchemaField("countryCode", "STRING"),
            bq.SchemaField("subdivisionCodes", "STRING", mode="REPEATED"),
            bq.SchemaField("nationalHoliday", "BOOLEAN"),
            bq.SchemaField("holidayTypes", "STRING", mode="REPEATED")
        ],
        create_disposition=bq.CreateDisposition.CREATE_IF_NEEDED
    )
    print("Loading holidays to BigQuery...")
    job = client.load_table_from_json(holidays_list, TABLE_NAME, job_config = job_config)
    print("Loading holidays was successful")
    
if __name__=="__main__":
    
    print("Connecting to the cloud")
    credentials = sa.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    client = bq.Client(credentials=credentials, project=PROJECT_ID)
    print("Connecting was successful")

    load_holidays_to_bigquery()
