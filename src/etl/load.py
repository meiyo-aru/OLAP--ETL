from data.connect_db_DW import connect_db_dw

dw_engine = connect_db_dw("AdventureWorksDW")

def load_aw(df):
    print("Carregando dados na tabela staging.stg_sales...")
    df = df.rename(columns={
        "FreightAmount": "freight_amount",
        "SalesOrderID": "sales_order_id",
        "OrderDate": "order_date",
        "DueDate": "due_date",
        "ShipDate": "ship_date",
        "CustomerID": "customer_id",
        "SalesPersonID": "salesperson_id",
        "TerritoryID": "territory_id",
        "SalesOrderDetailID": "sales_order_detail_id",
        "ProductID": "product_id",
        "OrderQty": "order_qty",
        "UnitPrice": "unit_price",
        "UnitPriceDiscount": "unit_price_discount",
        "LineTotal": "line_total",
        "Freight": "freight",
        "ProductName": "product_name",
        "ProductNumber": "product_number",
        "Category": "category",
        "Subcategory": "subcategory",
        "StandardCost": "standard_cost",
        "ListPrice": "list_price",
        "CustomerFullName": "full_name",
        "Email": "email",
        "Phone": "phone",
        "Address": "address",
        "City": "city",
        "State": "state",
        "Country": "country",
        # Novas colunas do staging
        "SalesAmount": "sales_amount",
        "CostAmount": "cost_amount",
        "ProfitAmount": "profit_amount",
        "DiscountAmount": "discount_amount"
    })
    # Carregar todos os campos necessários para staging
    df.to_sql('stg_sales', dw_engine, schema='staging', if_exists='append', index=False)
    print("Dados carregados com sucesso na tabela staging.stg_sales.")
