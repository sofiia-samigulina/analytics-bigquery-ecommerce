# Data Analysis of thelook_ecommerce dataset in Google BigQuery

## About the project

This project presents data analysis and engineering part of the "thelook_ecommerce" dataset in Google BigQuery. The dataset is synthetic. It contains 7 tables: products, distribution_centers, inventory_items, order_items, orders, events, users. The relational schema is shown below: 

[![Relational Schema thelook_ecommerce](/docs/diagrams/relational_schema_thelook_ecommerce.png)](/docs/diagrams/relational_schema_thelook_ecommerce.png)

During the data engineering phase I added a new table containing public holidays for the countries present in the dataset.

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

World holidays are pulled from the Calendarific REST API and loaded into the same layer. Public holidays come from the Calendarific REST API. The raw JSON response
is stored unparsed as a single STRING column, alongside the request parameters (country code and year) needed to identify it. 

Both paths run as a full refresh. Incremental loading in progress...

### Transformation (SQL)

All transformations run inside BigQuery, so the raw layer stays reproducible from its sources alone.

The holidays table is the substantial one: the stored JSON is parsed with PARSE_JSON, and the nested holidays array is expanded into one row per holiday with UNNEST and JSON_QUERY_ARRAY. Dates arrive in mixed formats (plain dates and full timestamps with offsets), so they are truncated to the date part before casting.

The remaining tables are cleaned without changing their grain: dropping unused columns, casting types, renaming for consistency (created_at becomes registration_date, ordered_at, received_at, occurred_at depending on what it means in context), and normalizing values that appear in more than one form (for example, country names).

### Orchestration

In progress...

### Prepared data for analytics

Actually contain business-level tables at the grain each question needs, joined and aggregated from staging. The reporting views keep the same names and columns as before, so the Power BI report does not change when the implementation underneath it does.

Rebuilding as a star schema to support a dynamic report in progress...

## Technologies

- Google BigQuery - data warehouse and query engine (public dataset "thelook_ecommerce")
- Python - data ingestion (google-cloud-bigquery, requests)
- REST API - API Calendarific, world holidays as an external source
- SQL - data transformation and analysis: aggregation functions, JOINs, order by, group by, CTEs, case when, having, views, JSON parsing
  with "UNNEST", partitioning and clustering
- Power BI Desktop: DAX measures, visualizations 
- ERDPlus: relational schema modeling


