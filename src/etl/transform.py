from data.connect_db_AW import aw_engine
import pandas as pd

def transform_aw(df):
    print('Iniciando transformação dos dados...')
    # Calcular campos derivados e normalizar nomes
    df['sales_amount'] = df['LineTotal']
    df['cost_amount'] = df['OrderQty'] * df['StandardCost']
    df['profit_amount'] = df['sales_amount'] - df['cost_amount']
    df['freight_amount'] = df['Freight']
    df['discount_amount'] = df['UnitPrice'] * df['OrderQty'] * df['UnitPriceDiscount']
    # Normalizar nomes para snake_case
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
    print('Transformação concluída.')
    return df