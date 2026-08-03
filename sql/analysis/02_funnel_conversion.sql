--question 2
--Where do we lose customers in the sales funnel and is there any difference by the browser?

WITH CTE_unique_session AS (
  SELECT session_id, ANY_VALUE(browser) AS browser,
  MAX(CASE WHEN event_type = 'product' THEN 1 ELSE 0 END) AS had_product,
  MAX(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS had_cart,
  MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS had_purchase
  FROM `bigquery-public-data.thelook_ecommerce.events` 
  GROUP BY session_id
)
SELECT CTE_unique_session.browser, COUNT(*) AS all_sessions, SUM(had_product) AS visited_product, SUM(had_cart) AS visited_cart, SUM(had_purchase) AS visited_purchase, 
ROUND(SAFE_DIVIDE(SUM(had_product), COUNT(*)) *100,2) AS visited_product_pct,
ROUND(SAFE_DIVIDE(SUM(had_cart), COUNT(*)) *100,2) AS visited_cart_pct,
ROUND(SAFE_DIVIDE(SUM(had_purchase), COUNT(*)) *100,2) AS visited_purchase_pct
FROM CTE_unique_session
GROUP BY CTE_unique_session.browser
HAVING COUNT(*) > 100
ORDER BY all_sessions DESC

--Chrome is the most popular browser, but funnel conversion is nearly identical across browsers.
--Every session in the dataset includes a product view. This is likely an artefact of the synthetic data rather than real behavior.
--62-64% reached a cart and 26-27% completed a purchase. 