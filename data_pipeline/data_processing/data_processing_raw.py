from google.oauth2 import service_account as sa
from google.cloud import bigquery as bq
from data_pipeline.constants import MY_PROJECT_ID, RAW_DATASET_ID, SERVICE_ACCOUNT_FILE
import pandas as pd
import country_converter as coco
import json

def download_raw_data_from_bigquery():
    datasets = {}
    tables = ["distribution_centers", "events", "holidays", "inventory_items", "order_items", "orders", "products", "users"]
    for table in tables:

        try:
            table_ref = client.get_table(f"{RAW_DATASET_ID}.{table}")
            df = client.list_rows(table_ref).to_dataframe(create_bqstorage_client=True)
            datasets[table] = df
            print(f"Downloaded {table} from BigQuery into DataFrame with {len(df)} rows.")
        except Exception as e:
            print(f"Failed to download {table}: {e}")

    return datasets

def transform_data(datasets):
    cc = coco.CountryConverter() #library for countries

    processed = {}

    if 'holidays' in datasets:
        holidays = datasets['holidays'].copy() 
        holidays['countryCode'] = holidays['countryCode'].str.upper()

        processed['holidays_clean'] = holidays
        print(f"Processed holidays data: {len(holidays)} rows")

    if 'users' in datasets:
        users = datasets['users'].copy() 

        # Remove time from 'created_at' column
        users['created_at'] = pd.to_datetime(users['created_at']).dt.date

        # Convert country names to ISO3 codes
        with open('country_fixes.json', 'r', encoding='utf-8') as f:
            manual_fixes = json.load(f)

        users['country'] = users['country'].replace(manual_fixes)
        users['country_code'] = cc.pandas_convert(series=users['country'], to='ISO2')
        not_found = users.loc[users['country_code'] == 'not found', 'country'].unique()
        print(not_found)

        processed['users_clean'] = users
        print(f"Processed users data: {len(users)} rows")

    if 'events' in datasets:
        events = datasets['events'].copy() 

        # Remove time from 'created_at' column
        events['created_at'] = pd.to_datetime(events['created_at']).dt.date

        processed['events_clean'] = events
        print(f"Processed events data: {len(events)} rows")

    if 'inventory_items' in datasets:
        inventory_items = datasets['inventory_items'].copy() 

        # Remove time from 'created_at' column
        inventory_items['created_at'] = pd.to_datetime(inventory_items['created_at']).dt.date

        # Remove time from 'sold_at' column
        inventory_items['sold_at'] = pd.to_datetime(inventory_items['sold_at']).dt.date

        processed['inventory_items_clean'] = inventory_items
        print(f"Processed inventory items data: {len(inventory_items)} rows")

    if 'order_items' in datasets:
        order_items = datasets['order_items'].copy() 

        # Remove time from 'created_at' column
        order_items['created_at'] = pd.to_datetime(order_items['created_at']).dt.date

        # Remove time from 'shipped_at' column
        order_items['shipped_at'] = pd.to_datetime(order_items['shipped_at']).dt.date

        # Remove time from 'delivered_at' column
        order_items['delivered_at'] = pd.to_datetime(order_items['delivered_at']).dt.date

        # Remove time from 'returned_at' column
        order_items['returned_at'] = pd.to_datetime(order_items['returned_at']).dt.date

        processed['order_items_clean'] = order_items
        print(f"Processed order items data: {len(order_items)} rows")

    if 'orders' in datasets:
        orders = datasets['orders'].copy() 

        # Remove time from 'created_at' column
        orders['created_at'] = pd.to_datetime(orders['created_at']).dt.date

        # Remove time from 'shipped_at' column
        orders['shipped_at'] = pd.to_datetime(orders['shipped_at']).dt.date

        # Remove time from 'delivered_at' column
        orders['delivered_at'] = pd.to_datetime(orders['delivered_at']).dt.date

        # Remove time from 'returned_at' column
        orders['returned_at'] = pd.to_datetime(orders['returned_at']).dt.date

        processed['orders_clean'] = orders
        print(f"Processed orders data: {len(orders)} rows")

    if 'products' in datasets:
        products = datasets['products'].copy() 

        processed['products_clean'] = products
        print(f"Processed products data: {len(products)} rows")

    if 'distribution_centers' in datasets:
        distribution_centers = datasets['distribution_centers'].copy()

        processed['distribution_centers_clean'] = distribution_centers
        print(f"Processed distribution centers data: {len(distribution_centers)} rows")

    return processed

def load_data_to_bigquery(processed_datasets):
    pass

def updated_transform_data():
    pass

if __name__=="__main__":
    credentials = sa.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    client = bq.Client(credentials=credentials, project=MY_PROJECT_ID)

    # 1 Extract
    #datasets = download_raw_data_from_bigquery()

    # 2 Transform
    #cleaned_datasets = transform_data(datasets)

    # 3 Load
    #load_data_to_bigquery(cleaned_datasets)