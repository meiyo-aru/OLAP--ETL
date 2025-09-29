from data.connect_db_DW import connect_db_dw

dw_engine = connect_db_dw("AdventureWorksDW")

def load_aw(df):
    df.to_sql('stg_sales', dw_engine, schema='staging', if_exists='append', index=False)
