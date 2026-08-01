CREATE OR REPLACE VIEW analytics_ecommerce.customers AS  
  SELECT u.id, ANY_VALUE(traffic_source) AS traffic_source,
  CASE WHEN COUNT(DISTINCT o.order_id) >= 2 THEN 1 ELSE 0 END AS had_two_or_more_orders, SUM(oi.sale_price) AS revenue_per_customer
  FROM `bigquery-public-data.thelook_ecommerce.users` u
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.orders` o ON u.id = o.user_id
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.order_items` oi ON o.order_id = oi.order_id
  GROUP BY u.id