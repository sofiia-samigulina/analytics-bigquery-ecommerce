from data_pipeline.data_processing.data_transformer import DataTransformer
from prefect import flow, task, get_run_logger

@task(name="transform_data")
def transform_data(transformer,logger):
    # 1 the main transforming for holidays data, because this data is in JSON format, we need to parse it and create a new table with the relevant information
    logger.info("Transforming holidays data...")
    transformer.transform_holidays()

    # 2 updating countries for users
    logger.info("Transforming users data...")
    transformer.transform_users()

    # 3 transforming products data, added gross_margin
    logger.info("Transforming products data...")
    transformer.transform_products()

    # 4 transforming distribution centers data
    logger.info("Transforming distribution centers data...")
    transformer.transform_distribution_centers()

    # 5 transforming orders data
    logger.info("Transforming orders data...")
    transformer.transform_orders()

    # 6 transforming order items data
    logger.info("Transforming order items data...")
    transformer.transform_order_items()

    # 7 transforming events data
    logger.info("Transforming events data...")
    transformer.transform_events()

    # 8 transforming inventory items data
    logger.info("Transforming inventory items data...")
    transformer.transform_inventory_items()

@flow(name="process_data_pipeline")
def process_data_pipeline():
    transformer = DataTransformer()
    logger = get_run_logger()

    logger.info("Starting the data pipeline orchestration flow...")
    transform_data(transformer, logger)
    logger.info("Data pipeline orchestration flow completed successfully.")

if __name__ == "__main__":
    process_data_pipeline()
        
    