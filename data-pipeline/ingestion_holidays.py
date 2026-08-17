import pandas as pd
import pandas_gbq as pdq
from google.oauth2 import service_account as sa
 
#project details
PROJECT_ID = 'project-1fe4418a-24e0-4804-a77'
DATASET_ID = 'raw_ecommerce'
TABLE_ID = 'holidays'
TABLE_NAME = f'{DATASET_ID}.{TABLE_ID}'

#credentials
SERVICE_ACCOUNT_FILE = 'project-1fe4418a-24e0-4804-a77-51304304a3ee.json' #path to service account file
credentials = sa.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

df = pd.read_csv("data/raw/holiday_calendar.csv")

pdq.to_gbq(df, TABLE_NAME, project_id=PROJECT_ID, if_exists = 'replace')

print("Data uploaded successfully to BigQuery")