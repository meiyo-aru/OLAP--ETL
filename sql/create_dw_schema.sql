-- Criação dos schemas
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS dw;

-- Tabela de datas (dim_date)
CREATE TABLE IF NOT EXISTS dw.dim_date (
  date_key INT PRIMARY KEY,
  date DATE NOT NULL,
  day INT,
  month INT,
  quarter INT,
  year INT,
  weekday TEXT,
  is_weekend BOOLEAN,
  fiscal_period TEXT
);

-- Produto (dim_product) - SCD2
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

-- Cliente (dim_customer)
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

-- Vendedor (dim_salesperson)
CREATE TABLE IF NOT EXISTS dw.dim_salesperson (
  salesperson_key SERIAL PRIMARY KEY,
  salesperson_id INT,
  full_name TEXT,
  hire_date DATE,
  sales_quota NUMERIC,
  commission_pct NUMERIC
);

-- Território (dim_territory)
CREATE TABLE IF NOT EXISTS dw.dim_territory (
  territory_key SERIAL PRIMARY KEY,
  territory_id INT,
  name TEXT,
  country_region TEXT,
  group_name TEXT
);

-- Fato de vendas (fact_sales)
CREATE TABLE IF NOT EXISTS dw.fact_sales (
  sales_fact_id BIGSERIAL PRIMARY KEY,
  sales_order_id INT,
  order_line_id INT,
  date_key INT REFERENCES dw.dim_date(date_key),
  product_key INT REFERENCES dw.dim_product(product_key),
  customer_key INT REFERENCES dw.dim_customer(customer_key),
  salesperson_key INT REFERENCES dw.dim_salesperson(salesperson_key),
  territory_key INT REFERENCES dw.dim_territory(territory_key),
  order_qty INT,
  sales_amount NUMERIC,
  discount_amount NUMERIC,
  tax_amount NUMERIC,
  freight_amount NUMERIC,
  cost_amount NUMERIC,
  profit_amount NUMERIC,
  loaded_at TIMESTAMP DEFAULT now(),
  CONSTRAINT uq_order_line UNIQUE(sales_order_id, order_line_id)
);
