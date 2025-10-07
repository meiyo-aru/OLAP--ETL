-- Tabela staging para linhas de vendas
CREATE TABLE IF NOT EXISTS staging.stg_sales_lines (
  sales_order_id INT,
  order_line_id INT,
  order_date DATE,
  due_date DATE,
  ship_date DATE,
  customer_id INT,
  salesperson_id INT,
  territory_id INT,
  product_id INT,
  order_qty INT,
  unit_price NUMERIC,
  unit_price_discount NUMERIC,
  line_total NUMERIC,
  standard_cost NUMERIC,
  list_price NUMERIC,
  tax_amount NUMERIC,
  freight_amount NUMERIC
);

-- Outras tabelas staging podem ser criadas conforme necessário para dimensões
