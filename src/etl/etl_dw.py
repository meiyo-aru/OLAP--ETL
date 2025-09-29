import pandas as pd
import pyodbc

from sqlalchemy import create_engine
import psycopg2
from datetime import datetime

dw_engine = create_engine('postgresql+psycopg2://postgres:1234@localhost:5432/AdventureWorksDW')
aw_engine = create_engine("mssql+pyodbc://@localhost/AdventureWorks2022?driver=ODBC+Driver+17+for+SQL+Server?trusted_connection=yes")

# 2) Extrair (exemplo: novas linhas de SalesOrderDetail e SalesOrderHeader)
query = '''
SELECT h.SalesOrderID, h.OrderDate, h.DueDate, h.ShipDate, h.CustomerID,
h.SalesPersonID, h.TerritoryID,
 d.SalesOrderDetailID, d.ProductID, d.OrderQty, d.UnitPrice,
d.UnitPriceDiscount, d.LineTotal
FROM Sales.SalesOrderHeader h
JOIN Sales.SalesOrderDetail d on h.SalesOrderID = d.SalesOrderID
WHERE h.OrderDate >= ?
'''
# parâmetro watermark
watermark = '2001-01-01' # exemplo: última data processada

df = pd.read_sql(query, aw_engine, params=[watermark])

# 3) Transformar
# calcular sales_amount, cost_amount, profit
# obter standard cost de produtos
prod_q = 'SELECT ProductID, StandardCost FROM Production.Product'
prods = pd.read_sql(prod_q, aw_engine)
df = df.merge(prods, on='ProductID', how='left')
df['sales_amount'] = df['LineTotal']
df['cost_amount'] = df['OrderQty'] * df['StandardCost']
df['profit_amount'] = df['sales_amount'] - df['cost_amount']

# 4) Carregar em staging no DW
df.to_sql('stg_sales_lines', dw_engine, schema='staging', if_exists='append',
index=False)
# 5) Processar staging -> dim/fact usando SQL no Postgres (UPSERT/SCD2)
# exemplo simples: upsert fact
with dw_engine.begin() as conn:
conn.execute('''
 INSERT INTO dw.fact_sales (...) SELECT ... FROM staging.stg_sales_lines
 ON CONFLICT (sales_order_id, order_line_id) DO UPDATE SET ...
 ''')
