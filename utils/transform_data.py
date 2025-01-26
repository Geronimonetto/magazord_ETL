import pandas as pd
import os

def transformar_csv_cliente(df, output_parquet):
    # Renomear a coluna 'id' para 'id_cliente'
    df.rename(columns={'id': 'id_cliente'}, inplace=True)
    
    # Combinar as colunas 'nome' e 'sobrenome' em uma nova coluna 'nome_cliente'
    df['nome_cliente'] = df['nome'] + ' ' + df['sobrenome']
    
    # Remover as colunas originais 'nome' e 'sobrenome'
    df.drop(columns=['nome', 'sobrenome'], inplace=True)
    
    # Adicionar colunas extras ou ajustes para compatibilidade com o banco (como 'email' e 'telefone')
    df['email'] = None  # Definindo como None, pode ser ajustado conforme necessidade
    df['telefone'] = None  # Definindo como None, pode ser ajustado conforme necessidade
    
    # Garantir que a coluna 'id_cliente' tenha o tipo correto para o banco (inteiro)
    df['id_cliente'] = df['id_cliente'].astype(int)
    
    # Salvar o DataFrame transformado em um arquivo Parquet
    df.to_parquet(output_parquet, index=False)

def transformar_csv_produto(df, output_parquet):
    # Renomear as colunas conforme necessário
    df.rename(columns={'id': 'id_produto', 'Nome': 'nome_produto', 'Descrição': 'categoria', 'Preço': 'preco'}, inplace=True)
    
    # Truncar a coluna 'categoria' para 50 caracteres
    df['categoria'] = df['categoria'].str.slice(0, 50)
    
    # Excluir outras colunas desnecessárias (se houver)
    df.drop(columns=[col for col in df.columns if col not in ['id_produto', 'nome_produto', 'categoria', 'preco']], inplace=True)
    
    # Salvar o DataFrame transformado em um arquivo Parquet
    df.to_parquet(output_parquet, index=False)

def transformar_csv_transacao(df, output_parquet):
    # Renomear as colunas conforme necessário
    df.rename(columns={'id_transacao': 'id_transacao', 'id_cliente': 'id_cliente', 'id_produto': 'id_produto', 'quantidade': 'quantidade', 'data_transacao': 'data_transacao'}, inplace=True)
    
    # Garantir que 'id_cliente' e 'id_produto' sejam inteiros
    df['id_cliente'] = df['id_cliente'].astype(int)
    df['id_produto'] = df['id_produto'].astype(int)
    
    # Garantir que 'quantidade' seja inteiro
    df['quantidade'] = df['quantidade'].astype(int)
    
    # Garantir que 'data_transacao' seja do tipo data (DATE)
    df['data_transacao'] = pd.to_datetime(df['data_transacao'], errors='coerce').dt.date
    
    # Salvar o DataFrame transformado em um arquivo Parquet
    df.to_parquet(output_parquet, index=False)
