from extract import extract_aw
from data.connect_db_AW import aw_engine
import pandas as pd


df = extract_aw()

prod_q = 'SELECT ProductID, StandardCost FROM Production.Product'
prods = pd.read_sql(prod_q, aw_engine)
df = df.merge(prods, on='ProductID', how='left')
df['sales_amount'] = df['LineTotal']
df['cost_amount'] = df['OrderQty'] * df['StandardCost']
df['profit_amount'] = df['sales_amount'] - df['cost_amount']
df['freight_amount'] = df['Freight']
df['discount_amount'] = df['UnitPrice'] * df['OrderQty'] * df['UnitPriceDiscount']