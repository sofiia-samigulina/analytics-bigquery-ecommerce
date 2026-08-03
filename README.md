# Data Analysis of thelook_ecommerce dataset in Google BigQuery

## About the project

This project presents data analysis of "thelook_ecommerce" dataset in Google BigQuery. The dataset is synthetic. Has 7 tables: products, distribution_centers, inventory_items, order_items, orders, events, users. The relational schema is located on the link: 

[Relational schema The Look ecommerce](/docs/diagrams/relational_schema_thelook_ecommerce.png).

## Questions

1. Are the categories that drive revenue also the most profitable?
2. Where do we lose customers in the sales funnel and is there any difference by browser?
3. Which channel brings the most valuable customers?

## Key finding

![Ranking by margin and revenue Dashboard](/powerbi/img/01-margin-category.png)

Given the provided data, ranking by margin and by revenue does not match. "Outerwear & Coats" has the highest revenue ($325505) but ranks 8th by margin (every dollar returns 55 cents), while "Blazers & Jackets" has the highest margin (every dollar returns 62 cents) on mid-range revenue ($74201). "Clothing Sets" ranks last by both.

I recommend giving more weight to "Blazers & Jackets" in the marketing strategy. 

[Findings and recommendations](/docs/findings_recommendations.md).

## Technologies

- Google BigQuery - data source and query engine (public dataset "thelook_ecommerce")
- SQL - data exploration, transformation and analysis: aggregation functions, JOINs, order by, group by, CTE, case when, having, views
- Power BI Desktop: DAX measures, visualizations 
- ERDPlus: relational schema modeling


