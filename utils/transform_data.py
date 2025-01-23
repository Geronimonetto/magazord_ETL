from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
from pyiceberg.types import StringType, IntegerType, FloatType, TimestampType
import pandas as pd

# Configurar o catálogo Iceberg
catalog_path = "file:./catalog"  # Substitua pelo caminho absoluto
catalog = load_catalog("hadoop", uri=catalog_path)

# Função para transformar e salvar o CSV de clientes em Iceberg
def transformar_csv_cliente_iceberg(df, table_name):
    # Renomear a coluna 'id' para 'id_cliente'
    df.rename(columns={'id': 'id_cliente'}, inplace=True)
    
    # Combinar as colunas 'nome' e 'sobrenome' em uma nova coluna 'nome_cliente'
    df['nome_cliente'] = df['nome'] + ' ' + df['sobrenome']
    
    # Remover as colunas originais 'nome' e 'sobrenome'
    df.drop(columns=['nome', 'sobrenome'], inplace=True)

    # Definir o esquema da tabela
    schema = Schema(
        {"id_cliente": IntegerType(), "nome_cliente": StringType()}
    )
    
    # Criar a tabela no Iceberg
    catalog.create_table(table_name, schema)

    # Escrever os dados no formato Iceberg
    output_path = f"{catalog_path}/{table_name}/data.parquet"
    df.to_parquet(output_path, index=False)

# Função para transformar e salvar o CSV de produtos em Iceberg
def transformar_csv_produto_iceberg(df, table_name):
    # Renomear as colunas conforme necessário
    df.rename(columns={'id': 'id_produto', 'Nome': 'nome_produto', 'Descrição': 'categoria', 'Preço': 'preco'}, inplace=True)

    # Definir o esquema da tabela
    schema = Schema(
        {"id_produto": IntegerType(), "nome_produto": StringType(), "categoria": StringType(), "preco": FloatType()}
    )

    # Criar a tabela no Iceberg
    catalog.create_table(table_name, schema)

    # Escrever os dados no formato Iceberg
    output_path = f"{catalog_path}/{table_name}/data.parquet"
    df.to_parquet(output_path, index=False)

# Função para transformar e salvar o CSV de transações em Iceberg
def transformar_csv_transacao_iceberg(df, table_name):
    # Renomear as colunas conforme necessário
    df.rename(columns={
        'id_transacao': 'id_transacao', 
        'id_cliente': 'id_cliente', 
        'id_produto': 'id_produto', 
        'quantidade': 'quantidade', 
        'data_transacao': 'data_transacao'
    }, inplace=True)

    # Definir o esquema da tabela
    schema = Schema(
        {"id_transacao": IntegerType(), "id_cliente": IntegerType(), "id_produto": IntegerType(), 
         "quantidade": IntegerType(), "data_transacao": TimestampType()}
    )

    # Criar a tabela no Iceberg
    catalog.create_table(table_name, schema)

    # Escrever os dados no formato Iceberg
    output_path = f"{catalog_path}/{table_name}/data.parquet"
    df.to_parquet(output_path, index=False)
