--question 3
--Are the categories that drive revenue also the most profitable?

SELECT p.category, 
ROUND(SUM(oi.sale_price),2) AS revenue, ROUND(SUM(p.cost),2) AS costs, ROUND(SUM(oi.sale_price)-SUM(p.cost),2) AS margin, 
ROUND( SAFE_DIVIDE((SUM(oi.sale_price)-SUM(p.cost)),SUM(oi.sale_price)) *100,2) AS margin_pct
FROM `bigquery-public-data.thelook_ecommerce.products` p
INNER JOIN `bigquery-public-data.thelook_ecommerce.order_items` oi ON p.id = oi.product_id AND oi.status = "Complete"
GROUP BY p.category
ORDER BY margin_pct DESC --or order by revenue desc for the first part of question

-- The dataset contains 26 product categories.
-- Gross margin varies substantially: from 61.81% ("Blazers & Jackets") down to
-- 37.53% ("Clothing Sets"), a spread of 24 percentage points.
-- Ranking by margin and by revenue does not match: "Outerwear & Coats" has the
-- highest revenue but ranks 8th by margin, while "Blazers & Jackets" has the
-- highest margin on mid-range revenue (15th).
-- "Clothing Sets" ranks last by both.
