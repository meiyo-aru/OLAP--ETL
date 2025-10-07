from data.connect_db_AW import aw_engine
import pandas as pd

def extract_aw():
    print("Extraindo dados do AdventureWorks2022...")
    query = """
        SELECT h.Freight, h.SalesOrderID, h.OrderDate, h.DueDate, h.ShipDate, h.CustomerID,
            h.SalesPersonID, h.TerritoryID,
            d.SalesOrderDetailID, d.ProductID, d.OrderQty, d.UnitPrice,
            d.UnitPriceDiscount, d.LineTotal,
            p.Name AS ProductName, p.ProductNumber, pc.Name AS Category, psc.Name AS Subcategory,
            p.StandardCost, p.ListPrice,
            per.FirstName + ' ' + per.LastName AS CustomerFullName, per.EmailPromotion AS Email, 
            NULL AS Phone, NULL AS Address, NULL AS City, NULL AS State, NULL AS Country
        FROM Sales.SalesOrderHeader h
        JOIN Sales.SalesOrderDetail d on h.SalesOrderID = d.SalesOrderID
        JOIN Production.Product p on d.ProductID = p.ProductID
        LEFT JOIN Production.ProductSubcategory psc on p.ProductSubcategoryID = psc.ProductSubcategoryID
        LEFT JOIN Production.ProductCategory pc on psc.ProductCategoryID = pc.ProductCategoryID
        LEFT JOIN Sales.Customer c on h.CustomerID = c.CustomerID
        LEFT JOIN Person.Person per on c.PersonID = per.BusinessEntityID
        WHERE h.OrderDate >= ?
    """

    df = pd.read_sql(query, aw_engine, params=("2001-01-01",))
    print("Extração concluída.")
    return df