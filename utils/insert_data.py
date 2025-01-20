import os
import pandas as pd
import psycopg2
from psycopg2 import sql

# Função para conectar ao banco de dados PostgreSQL
def conectar_banco():
    try:
        conn = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para inserir dados no banco de dados
def inserir_dados(conn, tabela, dados):
    try:
        cursor = conn.cursor()
        
        # Construir a consulta SQL dinâmica com base nas colunas do DataFrame
        colunas = ', '.join(dados.columns)
        valores = ', '.join(['%s'] * len(dados.columns))
        
        query = sql.SQL("INSERT INTO {}.{schema}.{tabela} ({colunas}) VALUES ({valores})").format(
            schema=sql.Identifier('public'),  # Esquema 'public'
            tabela=sql.Identifier(tabela),    # Nome da tabela
            colunas=sql.SQL(colunas),         # Colunas do DataFrame
            valores=sql.SQL(valores)        # Valores a serem inseridos
        )
        
        # Inserir os dados linha por linha
        for linha in dados.values:
            cursor.execute(query, tuple(linha))
        
        conn.commit()
        cursor.close()
        print(f"Dados inseridos com sucesso na tabela {tabela}.")
    except Exception as e:
        print(f"Erro ao inserir dados na tabela {tabela}: {e}")

# Função principal para ler arquivos CSV e inserir dados no banco
def inserir_dados_csv(diretorio):
    conn = conectar_banco()
    if conn is None:
        return
    
    # Iterar sobre os arquivos CSV no diretório
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".csv"):
            tabela = os.path.splitext(arquivo)[0]  # Nome da tabela baseado no nome do arquivo
            caminho_arquivo = os.path.join(diretorio, arquivo)
            
            # Ler o arquivo CSV com pandas
            dados = pd.read_csv(caminho_arquivo)
            
            # Inserir os dados no banco de dados
            inserir_dados(conn, tabela, dados)
    
    conn.close()

if __name__ == "__main__":
    diretorio = "C:/Users/geron/Documents/Python_estudos/magazord-ETL/data/Staged/cliente/"
    inserir_dados_csv(diretorio)
