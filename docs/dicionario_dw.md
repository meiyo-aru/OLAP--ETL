# Dicionário de Dados do Data Warehouse (Modelo Multidimensional)

Este dicionário descreve as tabelas, colunas e tipos de dados do Data Warehouse construído a partir do modelo estrela (star schema) para o projeto AdventureWorks.

---

## Tabela: staging.stg_sales
Tabela de staging para carga inicial dos dados extraídos e transformados.

| Coluna             | Tipo             | Descrição                                 |
|--------------------|------------------|-------------------------------------------|
| sales_order_id     | INT              | ID do pedido de venda                     |
| order_date         | DATE             | Data do pedido                            |
| due_date           | DATE             | Data de vencimento                        |
| ship_date          | DATE             | Data de envio                             |
| customer_id        | INT              | ID do cliente                             |
| salesperson_id     | INT              | ID do vendedor                            |
| territory_id       | INT              | ID do território                          |
| sales_order_detail_id | INT           | ID do item da linha do pedido             |
| product_id         | INT              | ID do produto                             |
| order_qty          | INT              | Quantidade do item                        |
| unit_price         | NUMERIC(12,2)    | Preço unitário                            |
| unit_price_discount| NUMERIC(12,2)    | Desconto unitário                         |
| line_total         | NUMERIC(12,2)    | Total da linha                            |
| freight            | NUMERIC(12,2)    | Frete                                     |
| product_name       | TEXT             | Nome do produto                           |
| product_number     | TEXT             | Código do produto                         |
| category           | TEXT             | Categoria do produto                      |
| subcategory        | TEXT             | Subcategoria do produto                   |
| standard_cost      | NUMERIC(12,2)    | Custo padrão do produto                   |
| list_price         | NUMERIC(12,2)    | Preço de tabela do produto                |
| full_name          | TEXT             | Nome completo do cliente                  |
| email              | TEXT             | Email do cliente                          |
| phone              | TEXT             | Telefone do cliente                       |
| address            | TEXT             | Endereço do cliente                       |
| city               | TEXT             | Cidade do cliente                         |
| state              | TEXT             | Estado do cliente                         |
| country            | TEXT             | País do cliente                           |
| sales_amount       | NUMERIC(12,2)    | Valor da venda                            |
| cost_amount        | NUMERIC(12,2)    | Valor do custo                            |
| profit_amount      | NUMERIC(12,2)    | Lucro                                     |
| discount_amount    | NUMERIC(12,2)    | Valor do desconto                         |
| freight_amount     | NUMERIC(12,2)    | Valor do frete                            |
| loaded_at          | TIMESTAMP        | Data/hora de carga                        |

---

## Tabela: dw.dim_date
Dimensão de datas para análise temporal.

| Coluna     | Tipo   | Descrição                  |
|------------|--------|----------------------------|
| date_key   | INT    | Chave surrogate da data    |
| date       | DATE   | Data                       |
| day        | INT    | Dia                        |
| month      | INT    | Mês                        |
| quarter    | INT    | Trimestre                  |
| year       | INT    | Ano                        |
| weekday    | TEXT   | Dia da semana              |
| is_weekend | BOOL   | Indica se é fim de semana  |

---

## Tabela: dw.dim_customer
Dimensão de clientes (SCD2 simplificado).

| Coluna      | Tipo   | Descrição                        |
|-------------|--------|----------------------------------|
| customer_key| SERIAL | Chave surrogate do cliente       |
| customer_id | INT    | ID do cliente (OLTP)             |
| full_name   | TEXT   | Nome completo                    |
| email       | TEXT   | Email                            |
| phone       | TEXT   | Telefone                         |
| address     | TEXT   | Endereço                         |
| city        | TEXT   | Cidade                           |
| state       | TEXT   | Estado                           |
| country     | TEXT   | País                             |
| is_current  | BOOL   | Registro atual (SCD2)            |

---

## Tabela: dw.dim_product
Dimensão de produtos (SCD2 simplificado).

| Coluna        | Tipo           | Descrição                        |
|---------------|----------------|----------------------------------|
| product_key   | SERIAL         | Chave surrogate do produto       |
| product_id    | INT            | ID do produto (OLTP)             |
| product_name  | TEXT           | Nome do produto                  |
| product_number| TEXT           | Código do produto                |
| category      | TEXT           | Categoria                        |
| subcategory   | TEXT           | Subcategoria                     |
| standard_cost | NUMERIC(12,2)  | Custo padrão                     |
| list_price    | NUMERIC(12,2)  | Preço de tabela                  |
| is_current    | BOOL           | Registro atual (SCD2)            |

---

## Tabela: dw.fact_sales
Fato de vendas (granularidade: item do pedido).

| Coluna           | Tipo           | Descrição                                 |
|------------------|----------------|-------------------------------------------|
| sales_order_id   | INT            | ID do pedido de venda                     |
| order_line_id    | INT            | ID da linha do pedido                     |
| date_key         | INT            | Chave surrogate da data                   |
| product_key      | INT            | Chave surrogate do produto                |
| customer_key     | INT            | Chave surrogate do cliente                |
| salesperson_key  | INT            | ID do vendedor                            |
| territory_key    | INT            | ID do território                          |
| order_qty        | INT            | Quantidade vendida                        |
| sales_amount     | NUMERIC(12,2)  | Valor da venda                            |
| discount_amount  | NUMERIC(12,2)  | Valor do desconto                         |
| freight_amount   | NUMERIC(12,2)  | Valor do frete                            |
| cost_amount      | NUMERIC(12,2)  | Valor do custo                            |
| profit_amount    | NUMERIC(12,2)  | Lucro                                     |
| loaded_at        | TIMESTAMP      | Data/hora de carga                        |

---
