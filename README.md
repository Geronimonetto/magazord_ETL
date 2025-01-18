<div align='center'>

![Magazord](image/logo-magazord.png)

</div>

# Teste para vaga de Engenheiro de Dados no Magazord.com.br
Este repositório tem como fim testar os candidatos para vaga de engenheiro de dados na empresa [Magazord](https://magazord.com.br).
> Para esta vaga buscamos alguém apaixonado por Dados e como disponibilizar de maneira estrutura e eficiente para tomada de decisão sobre esses dados!


## O teste

O objetivo deste teste é avaliar as habilidades técnicas do candidato na manipulação de grandes volumes de dados, desenvolvimento de pipelines, modelagem de dados, otimização de consultas, e compreensão de arquiteturas de dados modernas.

### Cenário do teste

Uma empresa fictícia, **DataMart**, precisa processar e organizar grandes volumes de dados para análise de vendas. O conjunto de dados contém informações brutas de transações realizadas por diferentes clientes, proveniente de múltiplas fontes. A tarefa do candidato é criar um pipeline de dados funcional para limpar, transformar, e armazenar os dados para uso analítico.

## Parte 1: Construção do Pipeline de Dados
Descrição:
 - Fonte de Dados: Um banco de dados PostgreSQL com tabelas simuladas (transações, clientes e produtos) e arquivos CSV fornecidos.
 - Requisitos:
   - Criar uma pipeline para:
     - **Extrair** dados do banco de dados e dos arquivos CSV.
     - **Transformar** os dados para:
      - Normalizar nomes de clientes (capitalizar).
      - Corrigir valores ausentes (e.g., preço médio para produtos com valores nulos).
      - Deduplicar registros.
     - Criar uma nova tabela agregada com:
      - Receita total por cliente.
      - Número total de transações por cliente.
      - Produto mais comprado por cliente.
     - **Carregar** os dados transformados em um banco de dados final ou um data warehouse (PostgreSQL ou SQLite).
   
**Arquivos:**

Fornecer:
 - 3 arquivos CSV simulados:
  - [**cliente.csv**](/cliente.csv): id_cliente, nome_cliente, email, telefone
  - [**produtos.csv**](produtos.csv): id_produto, nome_produto, categoria, preco
  - **transacoes.csv**: id_transacao, id_cliente, id_produto, quantidade, data_transacao (Arquivo particionado em 3 zips [transacoes_1](transacoes_1.zip), [transacoes_2](transacoes_2.zip) e [transacoes_3](transacoes_3.zip))
 - Script SQL com criação das tabelas iniciais para o banco de dados PostgreSQL:
```
-- Criação da tabela de clientes
CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    nome_cliente VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(15)
);

-- Criação da tabela de produtos
CREATE TABLE produtos (
    id_produto INT PRIMARY KEY,
    nome_produto VARCHAR(100),
    categoria VARCHAR(50),
    preco DECIMAL(10, 2)
);

-- Criação da tabela de transações
CREATE TABLE transacoes (
    id_transacao INT PRIMARY KEY,
    id_cliente INT REFERENCES clientes(id_cliente),
    id_produto INT REFERENCES produtos(id_produto),
    quantidade INT,
    data_transacao DATE
);
```

## Parte 2: Otimização e Documentação
Descrição:
 - Otimização:
   - Melhorar o desempenho do pipeline utilizando:
     - Indexação em tabelas relevantes.
     - Estratégias de particionamento ou paralelização no processo de transformação.
 - Documentação:
   - Fornecer um README.md contendo:
    - Passos para executar o pipeline.
    - Descrição do fluxo de trabalho.
    - Decisões técnicas tomadas e por quê.
  
## Parte 3: Consultas Analíticas
Descrição:
 - Crie as seguintes consultas no banco de dados final:
   - Receita total por categoria de produto.
   - Top 5 produtos mais vendidos em um período de tempo.
   - Número de clientes ativos (que fizeram pelo menos 1 compra) nos últimos 3 meses.
 - Explicar como as consultas podem ser otimizadas para grandes volumes de dados.
    
## Entregas Esperadas

> [!IMPORTANT]
> Código fonte do pipeline.

> [!IMPORTANT]
> Banco de dados final populado com os dados processados.

> [!IMPORTANT]
> Consultas SQL.

> [!IMPORTANT]
> README.md com instruções detalhadas para execução.

## Critérios de Avaliação:
 - Completude Técnica:
   - O pipeline atende aos requisitos funcionais?
   - As consultas fornecem os resultados corretos?
 - Qualidade do Código:
   - Estrutura e organização do código.
   - Tratamento de erros.
   - Uso de boas práticas de desenvolvimento.
 - Eficiência:
   - O pipeline e as consultas foram otimizados para desempenho?
 - Documentação:
   - O README fornece instruções claras e detalhadas?
 - Criatividade e Inovação:
   - O candidato usou estratégias diferenciadas para resolver os problemas?

## Envio do teste

* Suba o repositório no seu Github e envie o link diretamente para o seu recrutador.

Obs.: Não serão aceitos alterações após o envio.
