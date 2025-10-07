
from sqlalchemy import text


def populate_dim_date(pg_engine):
    print("Populando dw.dim_date...")
    with pg_engine.connect() as conn:
        try:
            conn.execute(text("""
                INSERT INTO dw.dim_date (date_key, date, day, month, quarter, year, weekday, is_weekend)
                SELECT DISTINCT
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
            print("Tabela dw.dim_date populada com sucesso!")
        except Exception as e:
            raise
        
def populate_dim_customer(pg_engine):
    print("Populando dw.dim_customer...")
    with pg_engine.connect() as conn:
        try:
            # SCD2 simplificado: só insere se não existe customer_id atual
            conn.execute(text("""
                INSERT INTO dw.dim_customer (customer_id, full_name, email, phone, address, city, state, country, is_current)
                SELECT DISTINCT
                    customer_id, full_name, email, phone, address, city, state, country, TRUE
                FROM staging.stg_sales s
                WHERE NOT EXISTS (
                    SELECT 1 FROM dw.dim_customer c
                    WHERE c.customer_id = s.customer_id AND c.is_current = TRUE
                );
            """))
            print("Tabela dw.dim_customer populada com sucesso!")
        except Exception as e:
            raise
        
def populate_dim_product(pg_engine):
    print("Populando dw.dim_product...")
    with pg_engine.connect() as conn:
        try:
            # SCD2 simplificado: só insere se não existe product_id atual
            conn.execute(text("""
                INSERT INTO dw.dim_product (product_id, product_name, product_number, category, subcategory, standard_cost, list_price, is_current)
                SELECT DISTINCT
                    product_id,
                    product_name,
                    product_number,
                    category,
                    subcategory,
                    standard_cost,
                    list_price,
                    TRUE
                FROM staging.stg_sales s
                WHERE NOT EXISTS (
                    SELECT 1 FROM dw.dim_product d
                    WHERE d.product_id = s.product_id AND d.is_current = TRUE
                );
            """))
            print("Tabela dw.dim_product populada com sucesso!")
        except Exception as e:
            raise
        
def populate_fact_sales(pg_engine):
    print("Populando dw.fact_sales...")
    with pg_engine.connect() as conn:
        try:
            # Buscar surrogate keys das dimensões
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
                SELECT DISTINCT
                    s.sales_order_id,
                    s.sales_order_detail_id AS order_line_id,
                    EXTRACT(YEAR FROM s.order_date) * 10000 +
                    EXTRACT(MONTH FROM s.order_date) * 100 +
                    EXTRACT(DAY FROM s.order_date) AS date_key,
                    dp.product_key,
                    dc.customer_key,
                    s.salesperson_id,
                    s.territory_id,
                    s.order_qty,
                    s.sales_amount,
                    s.discount_amount,
                    s.freight_amount,
                    s.cost_amount,
                    s.profit_amount
                FROM staging.stg_sales AS s
                JOIN dw.dim_product dp ON s.product_id = dp.product_id AND dp.is_current = TRUE
                JOIN dw.dim_customer dc ON s.customer_id = dc.customer_id AND dc.is_current = TRUE
                -- Para salesperson e territory, usar surrogate key se implementar dimensão
                ON CONFLICT (sales_order_id, order_line_id) DO UPDATE
                SET
                    order_qty      = EXCLUDED.order_qty,
                    sales_amount   = EXCLUDED.sales_amount,
                    discount_amount = EXCLUDED.discount_amount,
                    cost_amount    = EXCLUDED.cost_amount,
                    profit_amount  = EXCLUDED.profit_amount,
                    loaded_at      = now();
            """))
            print("Tabela dw.fact_sales populada com sucesso!")
        except Exception as e:
            raise   
