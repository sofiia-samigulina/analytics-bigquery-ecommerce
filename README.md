# Data Analysis of thelook_ecommerce dataset in Google BigQuery

## About the project

This project presents data analysis and engineering part of the "thelook_ecommerce" dataset in Google BigQuery. The dataset is synthetic. It contains 7 tables: products, distribution_centers, inventory_items, order_items, orders, events, users. The relational schema is shown below: 

[![Relational Schema thelook_ecommerce](/docs/diagrams/relational_schema_thelook_ecommerce.png)](/docs/diagrams/relational_schema_thelook_ecommerce.png)

## Questions

1. Are the categories that drive revenue also the most profitable?
2. Where do we lose customers in the sales funnel and is there any difference by browser?
3. Which channel brings the most valuable customers?

## Key finding

![Ranking by margin and revenue Dashboard](/powerbi/img/01-margin-category.png)

Given the provided data, ranking by margin and by revenue does not match. "Outerwear & Coats" has the highest revenue ($325505) but ranks 8th by margin (every dollar returns 55 cents), while "Blazers & Jackets" has the highest margin (every dollar returns 62 cents) on mid-range revenue ($74201). "Clothing Sets" ranks last by both.

I recommend giving more weight to "Blazers & Jackets" in the marketing strategy. 

[Findings and recommendations](/docs/findings_recommendations.md).

## Data pipeline

The project started as an SQL analysis on top of the public dataset. I later extended it into a pipeline so the analysis runs on data I load and transform myself. 

### Ingestion (Python)

Source tables are copied from the public dataset into my own raw dataset. Tables that grow over time (orders, order_items, events, inventory_items) are partitioned by date; dimension tables (products, users, distribution_centers) are loaded as a full refresh, since they are small and change slowly.

World holidays are pulled from the Calendarific REST API and loaded into the same layer. This is a different ingestion pattern from the daily incremental load, because holidays are known in advance and change once a year rather than every day.

### Transformation (Python)

This layer cleans and standardizes each source table without changing its grain: column selection, type casting, consistent naming, and normalization of inconsistent values (for example, country names appearing in more than one form).

### Orchestration

In progress...

### Prepared data for analytics

Actually contain business-level tables at the grain each question needs, joined and aggregated from staging. The reporting views keep the same names and columns as before, so the Power BI report does not change when the implementation underneath it does.

Rebuilding as a star schema to support a dynamic report in progress...

## Technologies

- Google BigQuery - data warehouse and query engine (public dataset "thelook_ecommerce")
- Python - data ingestion and transformation (google-cloud-bigquery, requests, pandas)
- REST API - API Calendarific, world holidays as an external source
- SQL - data exploration and analysis: aggregation functions, JOINs, order by, group by, CTE, case when, having, views
- Power BI Desktop: DAX measures, visualizations 
- ERDPlus: relational schema modeling


