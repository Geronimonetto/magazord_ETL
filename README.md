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

![Imagem do diagrama](https://i.imgur.com/kCbdNAY.png)

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

### 2. Execução do projeto
   ```bash
   docker-compose up
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

### Arquitetura de Dados
Este projeto segue uma arquitetura de dados em camadas, estruturada para otimizar a coleta, o processamento e a análise das informações.

Staging
A camada de staging é responsável por armazenar os dados brutos importados de diversas fontes. Esses dados são mantidos na forma original para garantir a integridade e a flexibilidade para transformações futuras.

Datamart
Após o processamento, os dados são transformados e organizados em datamarts, que são otimizados para consultas e análise. Os datamarts contêm dados específicos para diferentes áreas de negócio, como vendas, marketing e finanças.


### Camada de Staging.
![Camada staging](https://i.imgur.com/urqifmz.png)

### Camada de Datamart.
![Camada datamart](https://i.imgur.com/jAfc4SI.png)

---
Essa abordagem permite que os dados sejam acessados de forma eficiente, melhorando o desempenho das consultas e a análise.

# Conclusão
O projeto Magazord-ETL foi desenvolvido com o objetivo de criar um pipeline eficiente para o processamento de grandes volumes de dados de vendas, utilizando uma arquitetura robusta em camadas. A estratégia de utilizar uma abordagem ELT, onde as transformações são feitas diretamente no banco de dados com DBT Core, garante flexibilidade e escalabilidade ao processo de integração e transformação dos dados.

A separação em camadas de Staging e Datamart facilita a organização e o acesso rápido aos dados para análise, enquanto o uso de ferramentas como DuckDB, Python, DBT Core e PostgreSQL proporciona um ambiente eficiente e de fácil manutenção. A implementação de consultas analíticas, como a receita total por categoria de produto e o top 5 produtos mais vendidos, permite que a empresa extraia insights valiosos para decisões estratégicas.

Com a utilização do Docker para facilitar a configuração e o gerenciamento do banco de dados, além de práticas de otimização e indexação, o projeto está preparado para lidar com grandes volumes de dados de maneira rápida e eficaz.

Esta arquitetura garante a integridade dos dados, oferece flexibilidade para transformações futuras e melhora o desempenho nas consultas analíticas, permitindo que as equipes de dados possam tomar decisões informadas e com maior agilidade.

