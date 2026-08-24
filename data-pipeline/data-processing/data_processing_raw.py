from google.oauth2 import service_account as sa
from google.cloud import bigquery as bq

MY_PROJECT_ID = 'project-1fe4418a-24e0-4804-a77'
ECOMMERCE_DATASET_ID = 'bigquery-public-data.thelook_ecommerce'
DATASET_ID = 'raw_ecommerce'
SERVICE_ACCOUNT_FILE = 'data-pipeline/data-ingestion/service_account_credential.json' #path to service account file

def download_raw_data_from_bigquery():
    pass

if __name__=="__main__":
    credentials = sa.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    client = bq.Client(credentials=credentials, project=MY_PROJECT_ID)

    download_raw_data_from_bigquery()