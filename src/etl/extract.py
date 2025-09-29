from data.connect_db_AW import aw_engine
import pandas as pd

def extract_aw():
    query = '''
    SELECT h.Freight, h.SalesOrderID, h.OrderDate, h.DueDate, h.ShipDate, h.CustomerID,
    h.SalesPersonID, h.TerritoryID,
    d.SalesOrderDetailID, d.ProductID, d.OrderQty, d.UnitPrice,
    d.UnitPriceDiscount, d.LineTotal
    FROM Sales.SalesOrderHeader h
    JOIN Sales.SalesOrderDetail d on h.SalesOrderID = d.SalesOrderID
    WHERE h.OrderDate >= :watermark
    '''
    df = pd.read_sql(query, aw_engine, params={"watermark": "2001-01-01"})
    return df