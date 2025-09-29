from data.connect_db_DW import connect_db_dw
from src.etl.extract import extract_aw
from src.etl.populate import populate_fact_sales, populate_dim_customer, populate_dim_product, populate_dim_date
from src.etl.transform import transform_aw
from src.etl.load import load_aw

pg_engine = connect_db_dw("AdventureWorksDW")

df = extract_aw()
transform_aw(df)
load_aw(df)

populate_fact_sales(pg_engine)
populate_dim_date(pg_engine)
populate_dim_customer(pg_engine)
populate_dim_product(pg_engine)

