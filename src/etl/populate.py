
from sqlalchemy import text


def populate_dim_date(pg_engine):
    with pg_engine.connect() as conn:
        try:
            conn.execute(text("""
                INSERT INTO dw.dim_date (date_key, date, day, month, quarter, year, weekday, is_weekend)
                SELECT
                    EXTRACT(YEAR FROM order_date) * 10000 +
                    EXTRACT(MONTH FROM order_date) * 100 +
                    EXTRACT(DAY FROM order_date) AS date_key,
                    order_date AS date,
                    EXTRACT(DAY FROM order_date) AS day,
                    EXTRACT(MONTH FROM order_date) AS month,
                    EXTRACT(QUARTER FROM order_date) AS quarter,
                    EXTRACT(YEAR FROM order_date) AS year,
                    TO_CHAR(order_date, 'Day') AS weekday,
                    CASE WHEN EXTRACT(DOW FROM order_date) IN (0,6) THEN TRUE ELSE FALSE END AS is_weekend
                FROM staging.stg_sales
                ON CONFLICT (date_key) DO NOTHING;
            """))
        except Exception as e:
            raise
        
def populate_dim_customer(pg_engine):
    with pg_engine.connect() as conn:
        try:
            conn.execute(text("""
                INSERT INTO dw.dim_customer (customer_id, full_name, email, phone, address, city, state, country)
                SELECT DISTINCT
                    customer_id, full_name, email, phone, address, city, state, country
                FROM staging.stg_sales s
                WHERE NOT EXISTS (
                    SELECT 1 FROM dw.dim_customer c
                    WHERE c.customer_id = s.customer_id AND c.is_current = TRUE
                );
            """))
        except Exception as e:
            raise
        
def populate_dim_product(pg_engine):
    with pg_engine.connect() as conn:
        try:
            conn.execute(text("""
                INSERT INTO dw.dim_product (product_id, product_name, product_number, category, subcategory, standard_cost, list_price)
                SELECT DISTINCT
                    product_id,
                    product_name,
                    product_number,
                    category,
                    subcategory,
                    standard_cost,
                    list_price
                FROM staging.stg_sales s
                WHERE NOT EXISTS (
                    SELECT 1 FROM dw.dim_product d
                    WHERE d.product_id = s.product_id AND d.is_current = TRUE
                );
            """))
        except Exception as e:
            raise
        
def populate_fact_sales(pg_engine):
    with pg_engine.connect() as conn:
        try:
            conn.execute(text("""
                INSERT INTO dw.fact_sales (
                    sales_order_id,
                    order_line_id,
                    date_key,
                    product_key,
                    customer_key,
                    salesperson_key,
                    territory_key,
                    order_qty,
                    sales_amount,
                    discount_amount,
                    freight_amount,
                    cost_amount,
                    profit_amount
                )
                SELECT
                    s.sales_order_id,
                    s.sales_order_detail_id AS order_line_id,
                    -- Gerando a chave da dimensão de datas (YYYYMMDD)
                    EXTRACT(YEAR FROM s.order_date) * 10000 +
                    EXTRACT(MONTH FROM s.order_date) * 100 +
                    EXTRACT(DAY FROM s.order_date) AS date_key,
                    s.product_id,
                    s.customer_id,
                    s.salesperson_id,
                    s.territory_id,
                    s.order_qty,
                    s.sales_amount,
                    s.unit_price_discount AS discount_amount,
                    0 AS freight_amount,  -- Sem informação de frete, preenchendo com 0
                    s.cost_amount,
                    s.profit_amount
                FROM staging.stg_sales AS s
                ON CONFLICT (sales_order_id, order_line_id) DO UPDATE
                SET
                    order_qty      = EXCLUDED.order_qty,
                    sales_amount   = EXCLUDED.sales_amount,
                    discount_amount = EXCLUDED.discount_amount,
                    cost_amount    = EXCLUDED.cost_amount,
                    profit_amount  = EXCLUDED.profit_amount,
                    loaded_at      = now();
            """))
        except Exception as e:
            raise   
