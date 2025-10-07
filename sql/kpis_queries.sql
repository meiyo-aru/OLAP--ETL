-- KPI 1: Receita Total
SELECT SUM(sales_amount) AS total_sales
FROM dw.fact_sales
WHERE date_key BETWEEN 20240101 AND 20241231;

-- KPI 2: Número de Pedidos
SELECT COUNT(DISTINCT sales_order_id) AS orders_count
FROM dw.fact_sales
WHERE date_key BETWEEN 20240101 AND 20241231;

-- KPI 3: Ticket Médio
WITH orders AS (
  SELECT sales_order_id, SUM(sales_amount) AS order_total
  FROM dw.fact_sales
  WHERE date_key BETWEEN 20240101 AND 20241231
  GROUP BY sales_order_id
)
SELECT AVG(order_total) AS average_order_value FROM orders;

-- KPI 4: Unidades Vendidas
SELECT SUM(order_qty) AS units_sold
FROM dw.fact_sales
WHERE date_key BETWEEN 20240101 AND 20241231;

-- KPI 5: Margem Bruta
SELECT
  SUM(sales_amount) AS revenue,
  SUM(cost_amount) AS cost,
  (SUM(sales_amount) - SUM(cost_amount)) AS gross_margin_amount,
  (SUM(sales_amount) - SUM(cost_amount)) / NULLIF(SUM(sales_amount),0) AS gross_margin_pct
FROM dw.fact_sales
WHERE date_key BETWEEN 20240101 AND 20241231;

-- KPI 6: Crescimento Anual (YoY)
WITH per_year AS (
  SELECT (date_key/10000) AS year, SUM(sales_amount) as revenue
  FROM dw.fact_sales
  GROUP BY 1
)
SELECT
  y2024.revenue as revenue_2024,
  y2023.revenue as revenue_2023,
  (y2024.revenue - y2023.revenue)/NULLIF(y2023.revenue,0) as yoy_growth
FROM (SELECT revenue FROM per_year WHERE year=2024) y2024,
     (SELECT revenue FROM per_year WHERE year=2023) y2023;

-- KPI 7: Crescimento Mensal (MoM)
WITH per_month AS (
  SELECT (date_key/100) AS year_month, SUM(sales_amount) as revenue
  FROM dw.fact_sales
  GROUP BY 1
)
SELECT
  curr.year_month,
  curr.revenue as revenue_current,
  prev.revenue as revenue_prev,
  (curr.revenue - prev.revenue)/NULLIF(prev.revenue,0) as mom_growth
FROM per_month curr
LEFT JOIN per_month prev ON curr.year_month = prev.year_month + 1
ORDER BY curr.year_month;

-- KPI 8: Participação do Produto Mais Vendido na Receita Total
WITH product_revenue AS (
  SELECT dp.product_name, SUM(fs.sales_amount) AS revenue
  FROM dw.fact_sales fs
  JOIN dw.dim_product dp ON fs.product_key = dp.product_key
  GROUP BY dp.product_name
),
top_product AS (
  SELECT revenue FROM product_revenue ORDER BY revenue DESC LIMIT 1
),
total AS (
  SELECT SUM(revenue) AS total_revenue FROM product_revenue
)
SELECT 
  top_product.revenue AS top_product_revenue,
  (top_product.revenue / NULLIF(total.total_revenue,0)) AS top_product_pct
FROM top_product, total;

-- KPI 9: Taxa de Entrega no Prazo
SELECT SUM(CASE WHEN ship_date <= due_date THEN 1 ELSE 0 END)::float / COUNT(*) as on_time_rate
FROM staging.stg_sales
WHERE ship_date IS NOT NULL AND due_date IS NOT NULL;


-- KPI 10: Receita Média por Cliente
SELECT AVG(total_sales) AS avg_sales_per_customer
FROM (
  SELECT dc.customer_id, SUM(fs.sales_amount) AS total_sales
  FROM dw.fact_sales fs
  JOIN dw.dim_customer dc ON fs.customer_key = dc.customer_key
  GROUP BY dc.customer_id
) t;
