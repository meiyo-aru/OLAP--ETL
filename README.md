# 🛠️ Projeto ETL e Data Warehouse - AdventureWorks

## 📖 Sobre o Projeto
Este projeto tem como objetivo **construir um Data Warehouse** baseado no banco de dados **AdventureWorks**, utilizando **Python** para criar processos **ETL (Extract, Transform, Load)** e **PostgreSQL** como ambiente final para análise.  

O trabalho foi desenvolvido para consolidar conhecimentos em:
- Construção de **ETL's**
- **Modelagem dimensional** de dados (Star Schema)
- **Storytelling com dados**
- Criação e cálculo de **indicadores (KPIs)**
- Visualização de dados em **dashboards interativos**

---

## 🎯 Objetivos
1. Avaliar o modelo OLTP do **AdventureWorks** e entender sua estrutura.
2. Criar **10 indicadores estratégicos** para análise de negócio.
3. Propor e implementar um **modelo dimensional** no PostgreSQL.
4. Desenvolver uma **pipeline ETL** em Python para popular o DW.
5. Criar um **dashboard interativo** para análise dos KPIs.
6. Documentar todo o processo em artigo acadêmico, conforme guia da UNISALES.

---

## 🗂️ Estrutura do Projeto



OLAP-ETL/
│
├── data/
│   ├── connect_db_AW.py         # Conexão com SQL Server (fonte)
│   └── connect_db_DW.py         # Conexão e criação do DW (PostgreSQL)
│
├── src/
│   └── etl/
│       ├── extract.py           # Extração dos dados do SQL Server
│       ├── transform.py         # Transformação e cálculos
│       ├── load.py              # Carga no staging do DW
│       └── populate.py          # População das dimensões e fato
│
├── sql/
│   ├── create_dw_schema.sql     # Criação das tabelas do DW
│   ├── create_staging_tables.sql# Criação das tabelas staging
│   └── kpis_queries.sql         # Queries SQL dos KPIs
│
├── dashboard/
│   └── adventureworks_dashboard.pbix   # Dashboard Power BI (ou .py para Streamlit)
│
├── docs/
│   ├── modelo_dimensional.png         # Diagrama Star Schema
│   ├── dicionario_dw.md               # Dicionário de dados
│   └── projeto_artigo_unisales.md     # Artigo acadêmico
│
├── main.py                   # Pipeline ETL principal
├── requirements.txt          # Dependências Python
├── README.md                 # Documentação do projeto
└── .gitignore



---

## 🔧 Tecnologias Utilizadas
| Tecnologia | Finalidade |
|-------------|------------|
| **SQL Server** | Banco OLTP original (AdventureWorks) |
| **PostgreSQL** | Data Warehouse dimensional |
| **Python** | Construção da ETL |
| **Pandas** | Manipulação e transformação de dados |
| **SQLAlchemy** | Integração Python ↔ PostgreSQL |
| **PyODBC** | Conexão Python ↔ SQL Server |
| **Power BI** ou **Metabase** | Visualização e storytelling dos dados |

---

## 🏗️ Modelo Dimensional (Star Schema)
O modelo foi desenvolvido para otimizar a análise de vendas, clientes e produtos.  

**Fato principal:** `fact_sales`  
**Dimensões:**
- `dim_customer`  
- `dim_product`  
- `dim_date`  
- `dim_salesperson`  
- `dim_territory`

📌 **Objetivo:** facilitar análises por tempo, região, vendedor e produto.

![Modelo Dimensional](docs/modelo_dimensional.png)

---

## 📊 Indicadores (KPIs) Propostos
1. **Receita Total** – Soma de todas as vendas no período.
2. **Quantidade Total Vendida** – Total de itens vendidos.
3. **Ticket Médio** – Receita total ÷ número de pedidos.
4. **Vendas por Região** – Total de vendas agrupado por território.
5. **Top 5 Produtos Mais Vendidos** – Ranking por quantidade.
6. **Margem de Lucro Média** – `(Receita - Custo) / Receita`.
7. **Crescimento Mensal de Vendas** – Percentual de crescimento em relação ao mês anterior.
8. **Receita por Vendedor** – Total de vendas por representante.
9. **Percentual de Participação por Categoria** – Receita de cada categoria ÷ receita total.
10. **Churn de Clientes** – Percentual de clientes que não compraram em um período específico.

---


## 🖥️ Dashboard

O dashboard pode ser criado no **Power BI** (arquivo `.pbix`), **Metabase** ou **Streamlit**. Exemplos de páginas:

- Visão geral de vendas e KPIs
- Evolução temporal
- Análise por território e vendedor
- Produtos mais vendidos

> Exemplo Power BI: salve o arquivo em `dashboard/adventureworks_dashboard.pbix`.

> Exemplo Streamlit: crie um script Python em `dashboard/streamlit_app.py` usando pandas e plotly/matplotlib para ler os dados do DW e exibir os KPIs.

**Dica:** Use as queries do arquivo `sql/kpis_queries.sql` para alimentar os gráficos do dashboard.

---

## 🚀 Como Executar o Projeto

### **1. Pré-requisitos**

* Python 3.10+
* PostgreSQL instalado
* SQL Server instalado com banco AdventureWorks restaurado
* Pacotes Python (instalar com `pip install -r requirements.txt`)

---

### **2. Restaurar o AdventureWorks**

1. Abra o **SQL Server Management Studio (SSMS)**
2. Vá em **Databases → Restore Database**
3. Selecione o arquivo `.bak` do AdventureWorks
4. Clique em **OK**

---


at
### **3. Executar o main.py**

```bash
psql -U postgres -d AdventureWorksDW -f sql/create_dw_schema.sql
psql -U postgres -d AdventureWorksDW -f sql/create_staging_tables.sql
```

Ou execute `data/connect_db_DW.py` para criar o banco e as tabelas via Python.

---


## 🤝 Contribuidores

* **Seu Nome** - [GitHub](https://github.com/seuusuario)
* **Colega 2** - [GitHub](https://github.com/colega2)
* **Colega 3** - [GitHub](https://github.com/colega3)
* **Colega 4** - [GitHub](https://github.com/colega4)

---


## 📄 Licença

Este projeto é apenas para fins acadêmicos e não possui licença comercial.

```

