from google.oauth2 import service_account as sa
from google.cloud import bigquery as bq
from data_pipeline.constants import MY_PROJECT_ID, RAW_DATASET_ID, SERVICE_ACCOUNT_FILE, CLEANED_DATASET_ID

def transform_users():
    print("Transforming users data...")
    query = f"""
        CREATE OR REPLACE TABLE `{CLEANED_DATASET_ID}.users` AS
        SELECT 
            id as user_id,
            first_name,
            last_name,
            email,
            age,
            gender,
            CASE 
                WHEN country = "Brasil" THEN "Brazil" 
                WHEN country = "Deutschland" THEN "Germany"
                WHEN country = "España" THEN "Spain"
                ELSE country 
            END as country,
            postal_code,
            state,
            city,
            street_address,
            user_geom as user_location,
            traffic_source,
            DATE(created_at) as registration_date
        FROM 
            `{RAW_DATASET_ID}.users`
    """
    query_job = client.query(query)
    rows = query_job.result()  # Waits for query to finish
    print("Transforming users data was successful")

def transform_holidays():
    print("Transforming holidays data...")
    query = f"""
        CREATE OR REPLACE TABLE `{CLEANED_DATASET_ID}.holidays` AS
        SELECT 
            year as year,
            JSON_VALUE(holidays, '$.date.iso') as holiday_date,
            JSON_VALUE(holidays, '$.country.name') as country_name,
            UPPER(country_code) as country_code, 
            JSON_VALUE(holidays, '$.name') as holiday_name,
            JSON_VALUE(holidays, '$.description') as description, 
        FROM 
            `{RAW_DATASET_ID}.holidays`,
            UNNEST(JSON_QUERY_ARRAY(PARSE_JSON(payload), '$.response.holidays')) as holidays
    """
    query_job = client.query(query)
    rows = query_job.result()  # Waits for query to finish
    print("Transforming holidays data was successful")

def transform_products():
    print("Transforming products data...")
    query = f"""
        CREATE OR REPLACE TABLE `{CLEANED_DATASET_ID}.products` AS
        SELECT 
            id as product_id,
            cost,
            retail_price,
            retail_price - cost as gross_margin,
            category,
            name as product_name,
            brand,
            department,
            distribution_center_id
        FROM 
            `{RAW_DATASET_ID}.products`
    """
    query_job = client.query(query)
    rows = query_job.result()  # Waits for query to finish
    print("Transforming products data was successful")

def transform_distribution_centers():
    print("Transforming distribution centers data...")
    query = f"""
        CREATE OR REPLACE TABLE `{CLEANED_DATASET_ID}.distribution_centers` AS
        SELECT 
            id as distribution_center_id,
            name as distribution_center_name,
            distribution_center_geom as distribution_center_location
        FROM 
            `{RAW_DATASET_ID}.distribution_centers`
    """
    query_job = client.query(query)
    rows = query_job.result()  # Waits for query to finish
    print("Transforming distribution centers data was successful")

def transform_orders():
    print("Transforming orders data...")
    query = f"""
        CREATE OR REPLACE TABLE `{CLEANED_DATASET_ID}.orders` 
        PARTITION BY DATE_TRUNC(ordered_at, MONTH) AS
        SELECT 
            order_id, 
            user_id,
            status as order_status,
            gender,
            DATE(created_at) as ordered_at,
            DATE(returned_at) as returned_at,
            DATE(shipped_at) as shipped_at,
            DATE(delivered_at) as delivered_at,
            num_of_item
        FROM 
            `{RAW_DATASET_ID}.orders`
    """
    query_job = client.query(query)
    rows = query_job.result()  # Waits for query to finish
    print("Transforming orders data was successful")

def transform_order_items():
    print("Transforming order items data...")
    query = f"""
        CREATE OR REPLACE TABLE `{CLEANED_DATASET_ID}.order_items` 
        PARTITION BY DATE_TRUNC(ordered_at, MONTH) AS
        SELECT 
            id as order_item_id, 
            order_id,
            user_id,
            product_id,
            inventory_item_id,
            status as order_item_status,
            DATE(created_at) as ordered_at,
            DATE(returned_at) as returned_at,
            DATE(shipped_at) as shipped_at,
            DATE(delivered_at) as delivered_at,
            sale_price
        FROM 
            `{RAW_DATASET_ID}.order_items`
    """
    query_job = client.query(query)
    rows = query_job.result()  # Waits for query to finish
    print("Transforming order items data was successful")

def transform_events():
    print("Transforming events data...")
    query = f"""
        CREATE OR REPLACE TABLE `{CLEANED_DATASET_ID}.events` 
        PARTITION BY DATE_TRUNC(occurred_at, MONTH) AS
        SELECT 
            id as event_id,
            user_id,
            sequence_number,
            session_id,
            DATE(created_at) as occurred_at,
            ip_address,
            postal_code,
            state,
            city,
            browser,
            traffic_source,
            event_type
        FROM 
            `{RAW_DATASET_ID}.events`
    """
    query_job = client.query(query)
    rows = query_job.result()  # Waits for query to finish
    print("Transforming events data was successful")

def transform_inventory_items():
    print("Transforming inventory items data...")
    query = f"""
        CREATE OR REPLACE TABLE `{CLEANED_DATASET_ID}.inventory_items` 
        PARTITION BY DATE_TRUNC(received_at, MONTH) AS
        SELECT 
            id as inventory_item_id,
            product_id,
            DATE(created_at) as received_at,
            DATE(sold_at) as sold_at,
            TIMESTAMP_DIFF(sold_at, created_at, DAY) as days_in_stock,
            cost as product_cost,
            product_retail_price,
            product_retail_price - cost as product_gross_margin,
            product_category,
            product_name,
            product_brand,
            product_department,
            product_distribution_center_id as distribution_center_id
        FROM 
            `{RAW_DATASET_ID}.inventory_items`
    """
    query_job = client.query(query)
    rows = query_job.result()  # Waits for query to finish
    print("Transforming inventory items data was successful")

def transform_data():
    # 1
    # the main transforming for holidays data, because this data is in JSON format, we need to parse it and create a new table with the relevant information
    transform_holidays()

    # 2 updating countries for users
    transform_users()

    # 3 transforming products data, added gross_margin
    transform_products()

    # 4 transforming distribution centers data
    transform_distribution_centers()

    # 5 transforming orders data
    transform_orders()

    # 6 transforming order items data
    transform_order_items()

    # 7 transforming events data
    transform_events()

    # 8 transforming inventory items data
    transform_inventory_items()


if __name__=="__main__":
    credentials = sa.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    client = bq.Client(credentials=credentials, project=MY_PROJECT_ID)

    transform_data()