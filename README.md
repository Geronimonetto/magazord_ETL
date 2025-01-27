# Projeto Magazord-ETL

## Índice
1. [Visão Geral](#visão-geral)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Tempo de Processamento](#tempo-de-processamento)
4. [Ferramentas Utilizadas](#ferramentas-utilizadas)
5. [Diagrama do Projeto](#diagrama-do-projeto)
6. [Como Executar o Projeto](#como-executar-o-projeto)
    1. [Configuração do Docker](#1-configuração-do-docker)
    2. [Criação do Ambiente Virtual](#2-criação-do-ambiente-virtual)
    3. [Instalação das Dependências](#3-instalação-das-dependências)
    4. [Configuração do Banco de Dados](#4-configuração-do-banco-de-dados)
    5. [Execução do Pipeline](#5-execução-do-pipeline)
    6. [Execução do DBT](#6-execução-do-dbt)
7. [Consultas Analíticas](#consultas-analíticas)
8. [Decisões Técnicas](#decisões-técnicas)

## Visão Geral
O projeto Magazord-ETL foi desenvolvido para atender à necessidade de processar grandes volumes de dados de vendas, realizando a extração, transformação e carga (ETL) para posterior análise. Optou-se pelo uso da abordagem ELT, onde as transformações são realizadas diretamente no banco de dados utilizando o DBT Core.

Este projeto foca em três fontes principais:
- Dados simulados armazenados em PostgreSQL.
- Arquivos CSV.
- Transformações analíticas realizadas com DBT Core e Python.

## Estrutura do Projeto
A organização do projeto está definida conforme descrito abaixo:

- **main.py**: Realiza a extração, transformação e carga de dados em formato Parquet para posterior análise.
- **create_table.py**: Scripts para criação das tabelas no banco de dados PostgreSQL e inserção de dados oriundos de arquivos CSV.
- **transform_data.py**: Realiza transformações, incluindo normalização de nomes, correção de valores ausentes e deduplicação de registros.

## Tempo de Processamento
- **Tabela clientes**: 0,11 minutos
- **Tabela produtos**: 0,01 minutos
- **Tabela transações**: 3,90 minutos

## Ferramentas Utilizadas
As seguintes ferramentas foram escolhidas para garantir eficiência e escalabilidade do pipeline de dados:

- **DuckDB**: Banco de dados analítico em memória para consultas rápidas e eficientes.
- **DBT Core**: Para transformação e versionamento de dados com facilidade.
- **Python**: Linguagem principal para automação, manipulação de dados e integração.
- **Pandas**: Biblioteca essencial para limpeza, transformação e manipulação de dados tabulares.
- **Docker**: Isolamento do ambiente de execução e facilidade no gerenciamento do PostgreSQL.

## Diagrama do Projeto
O diagrama a seguir representa a arquitetura geral do projeto:

![Imagem do diagrama](https://imgur.com/kCbdNAY)

## Como Executar o Projeto

### 1. Configuração do Docker

#### Para Windows:
1. Abra o Docker Desktop e verifique se ele está em execução.
2. Caso não esteja, inicie-o e aguarde até que esteja pronto.

#### Para Linux:
1. Instale o Docker:
   ```bash
   sudo apt-get update
   sudo apt-get install docker.io
   ```
2. Inicie o Docker:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```
3. Verifique a instalação:
   ```bash
   docker --version
   ```

### 2. Criação do Ambiente Virtual

1. Navegue até o diretório do projeto.
2. Crie o ambiente virtual:
   - **Windows**:
     ```bash
     python -m venv venv
     ```
   - **Linux**:
     ```bash
     python3 -m venv venv
     ```

3. Ative o ambiente virtual:
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - **Linux**:
     ```bash
     source venv/bin/activate
     ```

### 3. Instalação das Dependências

Com o ambiente virtual ativado, instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

### 4. Configuração do Banco de Dados

1. Navegue até o diretório onde está localizado o arquivo `docker-compose.yml`.
2. Inicie o banco de dados PostgreSQL:
   ```bash
   docker-compose up -d
   ```
3. Verifique os contêineres em execução:
   ```bash
   docker ps
   ```

### 5. Execução do Pipeline

1. Com o ambiente virtual ativado, execute o script principal:
   ```bash
   python -m src.main
   ```

### 6. Execução do DBT

1. Navegue até o diretório do projeto DBT (`magazorddw`):
   ```bash
   cd magazorddw
   ```
2. Execute o comando para rodar as transformações:
   ```bash
   dbt run
   ```

## Consultas Analíticas

As consultas a seguir foram criadas para atender às necessidades analíticas do projeto:

1. **Receita total por categoria de produto:**
   ```sql
   SELECT categoria, SUM(preco * quantidade) AS receita_total
   FROM transacoes
   JOIN produtos ON transacoes.id_produto = produtos.id_produto
   GROUP BY categoria;
   ```

2. **Top 5 produtos mais vendidos em um período de tempo:**
   ```sql
   SELECT nome_produto, SUM(quantidade) AS total_vendido
   FROM transacoes
   JOIN produtos ON transacoes.id_produto = produtos.id_produto
   WHERE data_transacao BETWEEN '2024-01-01' AND '2024-12-31'
   GROUP BY nome_produto
   ORDER BY total_vendido DESC
   LIMIT 5;
   ```

3. **Número de clientes ativos nos últimos 3 meses:**
   ```sql
   SELECT COUNT(DISTINCT id_cliente) AS clientes_ativos
   FROM transacoes
   WHERE data_transacao >= CURRENT_DATE - INTERVAL '3 months';
   ```

## Decisões Técnicas

1. **Uso do DBT Core**: Centraliza e simplifica as transformações no banco de dados, facilitando a manutenção e escalabilidade.
2. **DuckDB**: Permite consultas rápidas e análises em memória para conjuntos de dados intermediários.
3. **PostgreSQL com Docker**: Proporciona uma solução local escalável e fácil de configurar.
4. **Indexação e Otimização**: Foram adicionados índices nas colunas de maior uso (e.g., `id_cliente` e `id_produto`) para melhorar o desempenho de consultas.

---

Este projeto foi desenvolvido com foco em eficiência, escalabilidade e boas práticas de engenharia de dados, garantindo soluções robustas e fáceis de manutenção. Para dúvidas ou melhorias, entre em contato!

