# Copilot Instructions for OLAP-ETL (AdventureWorks Data Warehouse)

## Project Overview
- This project implements a full ETL pipeline to build a dimensional Data Warehouse (DW) from the AdventureWorks OLTP database.
- Source: SQL Server (AdventureWorks)
- Target: PostgreSQL (Star Schema, fact and dimension tables)
- ETL: Python scripts using pandas, SQLAlchemy, and pyodbc
- Visualization: Power BI dashboard (see `dashboard/`)

## Key Components & Data Flow
- `data/connect_db_AW.py`: Connects to SQL Server (source)
- `data/connect_db_DW.py`: Connects to PostgreSQL (DW target), creates DW and tables
- `src/etl/extract.py`: Extracts data from SQL Server to pandas DataFrames
- `src/etl/transform.py`: Cleans and transforms extracted data
- `src/etl/load.py`: Loads transformed data into PostgreSQL staging tables
- `src/etl/populate.py`: Populates fact and dimension tables in DW from staging
- `main.py`: Orchestrates the ETL pipeline (connect, extract, transform, load, populate)

## Naming & Schema Conventions
- All table and column names in PostgreSQL are **lowercase with underscores** (e.g., `sales_order_id`).
- DataFrames extracted from SQL Server may have PascalCase columns; always rename to match DW schema before loading.
- Staging tables are in the `staging` schema; fact/dim tables in `dw` schema.

## Developer Workflow
1. Ensure SQL Server (with AdventureWorks) and PostgreSQL are running.
2. Run `main.py` to execute the full ETL pipeline.
3. If schema changes, update both SQL scripts in `sql/` and Python ETL scripts.
4. For new columns, update both DataFrame renaming and DW table definitions.
5. To reset DW, drop/recreate tables using `data/connect_db_DW.py` or `sql/create_dw.sql`.

## Integration Points
- **SQLAlchemy**: Used for all DB connections and DDL/DML in Python.
- **pyodbc**: Used for SQL Server connections.
- **pandas**: Used for all data manipulation and transfer between DBs.
- **Power BI**: Consumes data from PostgreSQL DW for dashboarding.

## Project-Specific Patterns
- Always populate `dim_date` before `fact_sales` to avoid FK errors.
- Use explicit column renaming in ETL to match DW schema.
- All ETL steps are modularized: extract, transform, load, populate.
- Use `if_exists='append'` in `to_sql` to avoid overwriting data.
- Foreign key constraints are enforced in DW; ensure referential integrity in ETL.

## Example: DataFrame Column Renaming
```python
# Before loading to DW, always rename columns:
df = df.rename(columns={
    "SalesOrderID": "sales_order_id",
    "OrderDate": "order_date",
    # ...
})
```

## Key Files/Directories
- `main.py`: Pipeline entrypoint
- `data/`: DB connection and setup scripts
- `src/etl/`: ETL logic (extract, transform, load, populate)
- `sql/`: DDL and KPI queries (if present)
- `dashboard/`: Power BI dashboard

---

For questions about workflow or architecture, see `README.md` or the ETL scripts for concrete examples.
