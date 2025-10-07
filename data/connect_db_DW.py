import psycopg2
from sqlalchemy import create_engine, text

def connect_db_dw(db_name="postgres"):
    try:
        engine = create_engine(
            f"postgresql+psycopg2://postgres:22609390aBCDE!@localhost:5432/{db_name}",
            isolation_level="AUTOCOMMIT" 
        )
        return engine
    except Exception as e: 
        raise
    
    
def create_db_dw():
    engine = connect_db_dw()

    with engine.connect() as conn:
        try:
            conn.execute(text('CREATE DATABASE "AdventureWorksDW";'))
            print("Banco Data Warehouse 'AdventureWorksDW' criado com sucesso!")
        except Exception as e:
            if 'already exists' in str(e):
                print("Banco já existe!")
            return False


    return True


def create_tables_dw():
    engine = connect_db_dw("AdventureWorksDW")
    print("Conexão com o Data Warehouse estabelecida!")

    with engine.connect() as conn:
        try:
            conn.execute(text(
            """
                -- criar schemas
                CREATE SCHEMA IF NOT EXISTS staging;
                CREATE TABLE IF NOT EXISTS staging.stg_sales (
                    freight_amount NUMERIC(12,2),
                    sales_order_id INT,
                    order_date DATE,
                    due_date DATE,
                    ship_date DATE,
                    customer_id INT,
                    salesperson_id INT,
                    territory_id INT,
                    sales_order_detail_id INT,
                    product_id INT,
                    order_qty INT,
                    unit_price NUMERIC(12,2),
                    unit_price_discount NUMERIC(12,2),
                    line_total NUMERIC(12,2),
                    freight NUMERIC(12,2),
                    product_name TEXT,
                    product_number TEXT,
                    category TEXT,
                    subcategory TEXT,
                    standard_cost NUMERIC(12,2),
                    list_price NUMERIC(12,2),
                    full_name TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    city TEXT,
                    state TEXT,
                    country TEXT,
                    sales_amount NUMERIC(12,2),
                    cost_amount NUMERIC(12,2),
                    profit_amount NUMERIC(12,2),
                    discount_amount NUMERIC(12,2),
                    loaded_at TIMESTAMP DEFAULT now()
                );
                CREATE SCHEMA IF NOT EXISTS dw;
                -- dim_date
                CREATE TABLE IF NOT EXISTS dw.dim_date (
                date_key INT PRIMARY KEY,
                date DATE NOT NULL,
                day INT,
                month INT,
                quarter INT,
                year INT,
                weekday TEXT,
                is_weekend BOOLEAN
                );
                -- dim_product (SCD2)
                CREATE TABLE IF NOT EXISTS dw.dim_product (
                product_key SERIAL PRIMARY KEY,
                product_id INT,
                product_name TEXT,
                product_number TEXT,
                category TEXT,
                subcategory TEXT,
                standard_cost NUMERIC,
                list_price NUMERIC,
                effective_start DATE DEFAULT CURRENT_DATE,
                effective_end DATE,
                is_current BOOLEAN DEFAULT TRUE
                );
                -- dim_customer
                CREATE TABLE IF NOT EXISTS dw.dim_customer (
                customer_key SERIAL PRIMARY KEY,
                customer_id INT,
                full_name TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                country TEXT,
                is_current BOOLEAN DEFAULT TRUE
                );
                -- fact_sales
                CREATE TABLE IF NOT EXISTS dw.fact_sales (
                sales_fact_id BIGSERIAL PRIMARY KEY,
                sales_order_id INT,
                order_line_id INT,
                date_key INT REFERENCES dw.dim_date(date_key),
                product_key INT REFERENCES dw.dim_product(product_key),
                customer_key INT REFERENCES dw.dim_customer(customer_key),
                salesperson_key INT,
                territory_key INT,
                order_qty INT,
                sales_amount NUMERIC,
                discount_amount NUMERIC,
                freight_amount NUMERIC,
                cost_amount NUMERIC,
                profit_amount NUMERIC,
                loaded_at TIMESTAMP DEFAULT now(),
                CONSTRAINT uq_order_line UNIQUE(sales_order_id, order_line_id)
                );
            """
            ))
            print("Tabelas do Data Warehouse criadas com sucesso!")
        except Exception as e:
            raise
    

create_db_dw()
create_tables_dw()