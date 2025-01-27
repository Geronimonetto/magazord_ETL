import pandas as pd
import os

def transformar_csv_cliente(df, output_parquet):
    # Renomear a coluna 'id' para 'id_cliente' e combinar 'nome' e 'sobrenome' em 'nome_cliente'
    df.rename(columns={'id': 'id_cliente'}, inplace=True)
    df['nome_cliente'] = (df['nome'] + ' ' + df['sobrenome']).str.strip().str.title()
    
    # Remover as colunas originais
    df.drop(columns=['nome', 'sobrenome'], inplace=True)
    
    # Adicionar colunas extras como 'email' e 'telefone'
    df['email'] = None
    df['telefone'] = None
    
    # Garantir que 'id_cliente' seja do tipo inteiro
    df['id_cliente'] = df['id_cliente'].astype(int)
    
    # Salvar o DataFrame em um arquivo Parquet
    df.to_parquet(output_parquet, index=False)

def transformar_csv_produto(df, output_parquet):
    # Renomear as colunas e truncar a 'categoria'
    df.rename(columns={'id': 'id_produto', 'Nome': 'nome_produto', 'Descrição': 'categoria', 'Preço': 'preco'}, inplace=True)
    df['categoria'] = df['categoria'].str.slice(0, 50)
    
    # Manter apenas as colunas necessárias
    df.drop(columns=[col for col in df.columns if col not in ['id_produto', 'nome_produto', 'categoria', 'preco']], inplace=True)
    
    # Salvar o DataFrame em um arquivo Parquet
    df.to_parquet(output_parquet, index=False)

def transformar_csv_transacao(df, output_parquet):
    # Renomear as colunas e garantir tipos de dados corretos
    df.rename(columns={'id_transacao': 'id_transacao', 'id_cliente': 'id_cliente', 'id_produto': 'id_produto', 'quantidade': 'quantidade', 'data_transacao': 'data_transacao'}, inplace=True)
    df['id_cliente'] = df['id_cliente'].astype(int)
    df['id_produto'] = df['id_produto'].astype(int)
    df['quantidade'] = df['quantidade'].astype(int)
    df['data_transacao'] = pd.to_datetime(df['data_transacao'], errors='coerce').dt.date
    
    # Salvar o DataFrame em um arquivo Parquet
    df.to_parquet(output_parquet, index=False)
