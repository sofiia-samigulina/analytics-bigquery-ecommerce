--question 2
--Which channel brings the most valuable customers?

WITH CTE_orders_count_by_user AS (
  SELECT u.id, ANY_VALUE(traffic_source) AS traffic_source,
  CASE WHEN COUNT(DISTINCT o.order_id) >= 2 THEN 1 ELSE 0 END AS had_two_or_more_orders, SUM(oi.sale_price) AS revenue_per_customer
  FROM `bigquery-public-data.thelook_ecommerce.users` u
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.orders` o ON u.id = o.user_id
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.order_items` oi ON o.order_id = oi.order_id
  GROUP BY u.id
)
SELECT traffic_source, COUNT(*) AS customers, SUM(had_two_or_more_orders) AS repeat_customers_count, 
ROUND(SAFE_DIVIDE(SUM(had_two_or_more_orders), COUNT(*)) *100, 2) AS repeat_rate_pct, ROUND(SUM(revenue_per_customer),2) AS total_revenue,
ROUND(SAFE_DIVIDE(SUM(revenue_per_customer), COUNT(*)), 2) AS avg_revenue_per_customer
FROM CTE_orders_count_by_user
GROUP BY traffic_source
ORDER BY avg_revenue_per_customer DESC

--The dataset has Email, Organic, Search, Display, Facebook channels. 
-- Avg revenue per customer ranges from $107 to $111 across the five channels,
-- a spread of approximately 4%. Given the difference in sample size between channels
-- (3,896 to 70,123 customers), this is too small to support a budget decision.
-- Channels differ primarily in volume, not in customer value.