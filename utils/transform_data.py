import pandas as pd
import os

def transformar_csv_cliente(df, output_parquet):
    # Renomear a coluna 'id' para 'id_cliente'
    df.rename(columns={'id': 'id_cliente'}, inplace=True)
    
    # Combinar as colunas 'nome' e 'sobrenome' em uma nova coluna 'nome_cliente'
    df['nome_cliente'] = df['nome'] + ' ' + df['sobrenome']
    
    # Remover as colunas originais 'nome' e 'sobrenome'
    df.drop(columns=['nome', 'sobrenome'], inplace=True)
    
    # Salvar o DataFrame transformado em um arquivo Parquet
    df.to_parquet(output_parquet, index=False)

def transformar_csv_produto(df, output_parquet):
    # Renomear as colunas conforme necessário
    df.rename(columns={'id': 'id_produto', 'Nome': 'nome_produto', 'Descrição': 'categoria', 'Preço': 'preco'}, inplace=True)
    
    # Salvar o DataFrame transformado em um arquivo Parquet
    df.to_parquet(output_parquet, index=False)

def transformar_csv_transacao(df, output_parquet):
    # Renomear as colunas conforme necessário
    df.rename(columns={'id_transacao': 'id_transacao', 'id_cliente': 'id_cliente', 'id_produto': 'id_produto', 'quantidade': 'quantidade', 'data_transacao': 'data_transacao'}, inplace=True)
    
    # Salvar o DataFrame transformado em um arquivo Parquet
    df.to_parquet(output_parquet, index=False)


