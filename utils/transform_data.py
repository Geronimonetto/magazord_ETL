import pandas as pd
import os

def transformar_csv_cliente(df, output_parquet):
    # Renomear a coluna 'id' para 'id_cliente' e combinar 'nome' e 'sobrenome' em 'nome_cliente'
    df.rename(columns={'id': 'id_cliente'}, inplace=True)
    df['nome_cliente'] = (df['nome'] + ' ' + df['sobrenome']).str.strip().str.title()
    
    # Remover as colunas originais de 'nome' e 'sobrenome', pois já não são mais necessárias
    df.drop(columns=['nome', 'sobrenome'], inplace=True)
    
    # Adicionar colunas extras como 'email' e 'telefone' com valores nulos
    df['email'] = None
    df['telefone'] = None
    
    # Garantir que a coluna 'id_cliente' seja do tipo inteiro
    df['id_cliente'] = df['id_cliente'].astype(int)
    
    # Salvar o DataFrame no formato Parquet, sem incluir o índice
    df.to_parquet(output_parquet, index=False)

def transformar_csv_produto(df, output_parquet):
    # Renomear as colunas e limitar o tamanho da 'categoria'
    df.rename(columns={'id': 'id_produto', 'Nome': 'nome_produto', 'Descrição': 'categoria', 'Preço': 'preco'}, inplace=True)
    df['categoria'] = df['categoria'].str.slice(0, 50)  # Truncar a categoria para 50 caracteres
    
    # Manter apenas as colunas necessárias para o produto
    df.drop(columns=[col for col in df.columns if col not in ['id_produto', 'nome_produto', 'categoria', 'preco']], inplace=True)
    
    # Salvar o DataFrame no formato Parquet, sem incluir o índice
    df.to_parquet(output_parquet, index=False)

def transformar_csv_transacao(df, output_parquet):
    # Renomear as colunas para garantir que as convenções de nomenclatura estejam consistentes
    df.rename(columns={'id_transacao': 'id_transacao', 'id_cliente': 'id_cliente', 'id_produto': 'id_produto', 'quantidade': 'quantidade', 'data_transacao': 'data_transacao'}, inplace=True)
    
    # Garantir que as colunas id_cliente e id_produto sejam do tipo inteiro
    df['id_cliente'] = df['id_cliente'].astype(int)
    df['id_produto'] = df['id_produto'].astype(int)
    df['quantidade'] = df['quantidade'].astype(int)
    
    # Converter a coluna 'data_transacao' para o formato de data, com tratamento de erros
    df['data_transacao'] = pd.to_datetime(df['data_transacao'], errors='coerce').dt.date
    
    # Salvar o DataFrame no formato Parquet, sem incluir o índice
    df.to_parquet(output_parquet, index=False)
