from google.oauth2 import service_account as sa
from google.cloud import bigquery as bq
from data_pipeline.constants import MY_PROJECT_ID, RAW_DATASET_ID, SERVICE_ACCOUNT_FILE, CLEANED_DATASET_ID

class DataTransformer:
    def __init__(self):
        self.credentials = sa.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        self.client = bq.Client(credentials=self.credentials, project=MY_PROJECT_ID)
        self.query = None
        self.query_job = None
        self.rows = None

    def transform_users(self):
        self.query = f"""
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
        self.query_job = self.client.query(self.query)
        self.rows = self.query_job.result()  # Waits for query to finish

    def transform_holidays(self):
        self.query = f"""
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
        self.query_job = self.client.query(self.query)
        self.rows = self.query_job.result()  # Waits for query to finish

    def transform_products(self):
        self.query = f"""
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
        self.query_job = self.client.query(self.query)
        self.rows = self.query_job.result()  # Waits for query to finish

    def transform_distribution_centers(self):
        self.query = f"""
            CREATE OR REPLACE TABLE `{CLEANED_DATASET_ID}.distribution_centers` AS
            SELECT 
                id as distribution_center_id,
                name as distribution_center_name,
                distribution_center_geom as distribution_center_location
            FROM 
                `{RAW_DATASET_ID}.distribution_centers`
        """
        self.query_job = self.client.query(self.query)
        self.rows = self.query_job.result()  # Waits for query to finish

    def transform_orders(self):
        self.query = f"""
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
        self.query_job = self.client.query(self.query)
        self.rows = self.query_job.result()  # Waits for query to finish

    def transform_order_items(self):
        self.query = f"""
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
        self.query_job = self.client.query(self.query)
        self.rows = self.query_job.result()  # Waits for query to finish
    
    def transform_events(self):
        self.query = f"""
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
        self.query_job = self.client.query(self.query)
        self.rows = self.query_job.result()  # Waits for query to finish

    def transform_inventory_items(self):
        self.query = f"""
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
        self.query_job = self.client.query(self.query)
        self.rows = self.query_job.result()  # Waits for query to finish