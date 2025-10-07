import pyodbc
from sqlalchemy import create_engine

# Conexão com instância padrão do SQL Server
# conn = pyodbc.connect(
#     "DRIVER={ODBC Driver 17 for SQL Server};"
#     "SERVER=localhost;"           
#     "DATABASE=AdventureWorks2022;"
#     "Trusted_Connection=yes;"     
# )

aw_engine = create_engine("mssql+pyodbc://@localhost/AdventureWorks2022?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes")

print("Conexão com AdventureWorks2019 estabelecida!")