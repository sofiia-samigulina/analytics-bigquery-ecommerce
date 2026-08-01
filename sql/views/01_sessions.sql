CREATE OR REPLACE VIEW analytics_ecommerce.sessions AS  
  SELECT session_id, ANY_VALUE(browser) AS browser,
  MAX(CASE WHEN event_type = 'product' THEN 1 ELSE 0 END) AS had_product,
  MAX(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS had_cart,
  MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS had_purchase
  FROM `bigquery-public-data.thelook_ecommerce.events` 
  GROUP BY session_id