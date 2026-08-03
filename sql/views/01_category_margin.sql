CREATE OR REPLACE VIEW analytics_ecommerce.category_margin AS  
  SELECT p.category, 
  ROUND(SUM(oi.sale_price),2) AS revenue, ROUND(SUM(p.cost),2) AS costs, ROUND(SUM(oi.sale_price)-SUM(p.cost),2) AS margin
  FROM `bigquery-public-data.thelook_ecommerce.products` p
  INNER JOIN `bigquery-public-data.thelook_ecommerce.order_items` oi ON p.id = oi.product_id AND oi.status = "Complete"
  GROUP BY p.category