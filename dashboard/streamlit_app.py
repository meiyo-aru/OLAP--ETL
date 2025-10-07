import streamlit as st
import pandas as pd
import sqlalchemy

# Configuração da conexão (ajuste para seu ambiente)
engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:22609390aBCDE!@localhost:5432/AdventureWorksDW')

st.title('Dashboard AdventureWorks - KPIs')



# Seletor de ano disponível
anos_df = pd.read_sql('SELECT DISTINCT (date_key/10000)::int AS ano FROM dw.fact_sales ORDER BY ano', engine)
anos = anos_df['ano'].tolist()
ano = st.selectbox('Selecione o ano', anos, index=0)
ano_anterior = ano - 1

# KPI 1: Receita Total
total_sales = pd.read_sql(f'SELECT SUM(sales_amount) AS total_sales FROM dw.fact_sales WHERE date_key BETWEEN {ano}0101 AND {ano}1231', engine).iloc[0,0]
total_sales = float(total_sales or 0)
st.metric(f'Receita Total ({ano})', f'R$ {total_sales:,.2f}')

# KPI 2: Número de Pedidos
orders_count = pd.read_sql(f'SELECT COUNT(DISTINCT sales_order_id) AS orders_count FROM dw.fact_sales WHERE date_key BETWEEN {ano}0101 AND {ano}1231', engine).iloc[0,0]
orders_count = pd.to_numeric(orders_count, errors='coerce')
orders_count = int(orders_count) if not pd.isna(orders_count) else 0
st.metric(f'Número de Pedidos ({ano})', orders_count)

# KPI 3: Ticket Médio
avg_order = pd.read_sql(f'''WITH orders AS (SELECT sales_order_id, SUM(sales_amount) AS order_total FROM dw.fact_sales WHERE date_key BETWEEN {ano}0101 AND {ano}1231 GROUP BY sales_order_id) SELECT AVG(order_total) AS average_order_value FROM orders''', engine).iloc[0,0]
avg_order = pd.to_numeric(avg_order, errors='coerce')
avg_order = float(avg_order) if not pd.isna(avg_order) else 0.0
st.metric(f'Ticket Médio ({ano})', f'R$ {avg_order:,.2f}')

# KPI 4: Unidades Vendidas
units_sold = pd.read_sql(f'SELECT SUM(order_qty) AS units_sold FROM dw.fact_sales WHERE date_key BETWEEN {ano}0101 AND {ano}1231', engine).iloc[0,0]
units_sold = pd.to_numeric(units_sold, errors='coerce')
units_sold = int(units_sold) if not pd.isna(units_sold) else 0
st.metric(f'Unidades Vendidas ({ano})', units_sold)

# KPI 5: Margem Bruta
margin = pd.read_sql(f'''SELECT SUM(sales_amount) AS revenue, SUM(cost_amount) AS cost, (SUM(sales_amount) - SUM(cost_amount)) AS gross_margin_amount, (SUM(sales_amount) - SUM(cost_amount)) / NULLIF(SUM(sales_amount),0) AS gross_margin_pct FROM dw.fact_sales WHERE date_key BETWEEN {ano}0101 AND {ano}1231''', engine)
gross_margin_amount = pd.to_numeric(margin["gross_margin_amount"][0], errors='coerce')
gross_margin_amount = float(gross_margin_amount) if not pd.isna(gross_margin_amount) else 0.0
gross_margin_pct = pd.to_numeric(margin["gross_margin_pct"][0], errors='coerce')
gross_margin_pct = float(gross_margin_pct) if not pd.isna(gross_margin_pct) else 0.0
st.metric(f'Margem Bruta (R$)', f'R$ {gross_margin_amount:,.2f}')
st.metric(f'Margem Bruta (%)', f'{gross_margin_pct*100:.2f}%')

# KPI 6: Crescimento Anual (YoY)
yoy = pd.read_sql(f'''
    WITH per_year AS (
        SELECT (date_key/10000) AS year, SUM(sales_amount) as revenue
        FROM dw.fact_sales
        GROUP BY 1
    )
    SELECT y_atual.revenue as revenue_atual, y_ant.revenue as revenue_ant, 
           (y_atual.revenue - y_ant.revenue)/NULLIF(y_ant.revenue,0) as yoy_growth
    FROM (SELECT revenue FROM per_year WHERE year={ano}) y_atual,
         (SELECT revenue FROM per_year WHERE year={ano_anterior}) y_ant
''', engine)
if not yoy.empty and 'yoy_growth' in yoy.columns:
    yoy_growth = pd.to_numeric(yoy.loc[0, "yoy_growth"], errors='coerce')
    yoy_growth = float(yoy_growth) if not pd.isna(yoy_growth) else 0.0
else:
    yoy_growth = 0.0
st.metric(f'Crescimento Anual (YoY)', f'{yoy_growth*100:.2f}%')

# KPI 7: Crescimento Mensal (MoM)
mom = pd.read_sql(f'''
    WITH per_month AS (
        SELECT (date_key/100) AS year_month, SUM(sales_amount) as revenue
        FROM dw.fact_sales
        WHERE (date_key/10000) = {ano}
        GROUP BY 1
    )
    SELECT curr.year_month, curr.revenue as revenue_current, prev.revenue as revenue_prev,
           (curr.revenue - prev.revenue)/NULLIF(prev.revenue,0) as mom_growth
    FROM per_month curr
    LEFT JOIN per_month prev ON curr.year_month = prev.year_month + 1
    ORDER BY curr.year_month
''', engine)
st.subheader(f'Crescimento Mensal (MoM) - {ano}')
if not mom.empty and 'mom_growth' in mom.columns:
    st.line_chart(mom.set_index('year_month')['mom_growth'])
else:
    st.write('Sem dados suficientes para o gráfico de crescimento mensal.')

# KPI 8: Participação do Produto Mais Vendido na Receita Total
top_prod = pd.read_sql(f'''
    WITH product_revenue AS (
        SELECT dp.product_name, SUM(fs.sales_amount) AS revenue
        FROM dw.fact_sales fs
        JOIN dw.dim_product dp ON fs.product_key = dp.product_key
        WHERE fs.date_key BETWEEN {ano}0101 AND {ano}1231
        GROUP BY dp.product_name
    ),
    top_product AS (
        SELECT revenue FROM product_revenue ORDER BY revenue DESC LIMIT 1
    ),
    total AS (
        SELECT SUM(revenue) AS total_revenue FROM product_revenue
    )
    SELECT top_product.revenue AS top_product_revenue,
           (top_product.revenue / NULLIF(total.total_revenue,0)) AS top_product_pct
    FROM top_product, total
''', engine)
top_product_pct = pd.to_numeric(top_prod["top_product_pct"][0], errors='coerce') if not top_prod.empty else 0.0
top_product_pct = float(top_product_pct) if not pd.isna(top_product_pct) else 0.0
st.metric(f'Participação do Produto Mais Vendido ({ano})', f'{top_product_pct*100:.2f}%')

# KPI 9: Taxa de Entrega no Prazo
on_time = pd.read_sql(f'''
        SELECT SUM(CASE WHEN ship_date <= due_date THEN 1 ELSE 0 END)::float / COUNT(*) as on_time_rate
        FROM staging.stg_sales
        WHERE ship_date IS NOT NULL AND due_date IS NOT NULL
            AND EXTRACT(YEAR FROM order_date) = {ano}
''', engine).iloc[0,0]
on_time = pd.to_numeric(on_time, errors='coerce')
on_time = float(on_time) if not pd.isna(on_time) else 0.0
st.metric(f'Taxa de Entrega no Prazo ({ano})', f'{on_time*100:.2f}%')

# KPI 10: Receita Média por Cliente
avg_cust = pd.read_sql(f'''
    SELECT AVG(total_sales) AS avg_sales_per_customer
    FROM (
        SELECT dc.customer_id, SUM(fs.sales_amount) AS total_sales
        FROM dw.fact_sales fs
        JOIN dw.dim_customer dc ON fs.customer_key = dc.customer_key
        WHERE fs.date_key BETWEEN {ano}0101 AND {ano}1231
        GROUP BY dc.customer_id
    ) t
''', engine).iloc[0,0]
avg_cust = pd.to_numeric(avg_cust, errors='coerce')
avg_cust = float(avg_cust) if not pd.isna(avg_cust) else 0.0
st.metric(f'Receita Média por Cliente ({ano})', f'R$ {avg_cust:,.2f}')

# Evolução Mensal de Receita (gráfico)
monthly = pd.read_sql(f'''
    SELECT (date_key/100) AS year_month, SUM(sales_amount) as revenue
    FROM dw.fact_sales
    WHERE (date_key/10000) = {ano}
    GROUP BY 1 ORDER BY 1
''', engine)
st.subheader(f'Evolução Mensal de Receita - {ano}')
if not monthly.empty:
    st.line_chart(monthly.set_index('year_month'))
else:
    st.write('Sem dados para o gráfico de evolução mensal.')

st.caption('Fonte: AdventureWorks Data Warehouse')
