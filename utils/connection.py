import os
import pandas as pd
import duckdb
from pathlib import Path
import psycopg2
from concurrent.futures import ThreadPoolExecutor

# Caminho relativo ao diretório do script ou diretório atual
base_path = Path(__file__).parent if '__file__' in globals() else Path.cwd()

# Voltando para o diretório pai (onde está a pasta 'data')
data_path = base_path.parent / 'data'

class DataLoader:
    def __init__(self, source_type, source_path):
        """
        Inicializa o DataLoader.
        :param source_type: Tipo de fonte de dados ('csv' ou 'db').
        :param source_path: Caminho para os dados. Para 'csv' é o diretório, 
                            para 'db' é o nome do banco de dados ou schema.
        """
        self.source_type = source_type
        self.source_path = source_path

    def load(self, table_name):
        """
        Função para carregar os dados de acordo com o tipo, CSV ou Database.
        :param table_name: Nome do arquivo CSV ou tabela do banco de dados.
        :return: DataFrame com os dados carregados.
        """
        try:
            if self.source_type == 'csv':
                return self._load_from_csv(table_name)
            elif self.source_type == 'db':
                return self._load_from_db(table_name)
            else:
                raise ValueError("Tipo de fonte não suportado. Use 'csv' ou 'db'.")
        except Exception as e:
            print(f"Erro ao carregar os dados: {e}")
            return None

    def _load_from_csv(self, table_name):
        """
        Carregar dados a partir de arquivos CSV usando DuckDB.
        :param table_name: Nome do arquivo CSV.
        :return: DataFrame com os dados carregados.
        """
        try:
            file_path = data_path / table_name  # Caminho ajustado para a pasta 'data'
            print(f"Caminho do arquivo: {file_path}")  # Depuração para garantir que o caminho está correto
            if not file_path.exists():
                raise FileNotFoundError(f"O arquivo {file_path} não foi encontrado.")
            
            # Usando DuckDB para carregar o CSV diretamente em um DataFrame
            conn = duckdb.connect()  # Conexão em memória
            query = f"SELECT * FROM read_csv_auto('{file_path}')"
            df = conn.execute(query).fetchdf()
            conn.close()  # Fechar a conexão com DuckDB
            return df
        except FileNotFoundError as e:
            print(f"Erro: {e}")
            return None
        except Exception as e:
            print(f"Erro ao carregar o CSV: {e}")
            return None

    def _load_from_db(self, table_name):
        """
        Carregar dados do banco de dados (aqui você pode implementar sua lógica de banco).
        :param table_name: Nome da tabela no banco de dados.
        :return: DataFrame com os dados carregados.
        """
        try:
            # Conectar ao banco de dados
            connection = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
            query = f"SELECT * FROM {self.source_path}.{table_name};"  # Considerando que source_path é o schema
            print(f"Carregando dados da tabela {table_name} do banco de dados...")
            df = pd.read_sql(query, connection)
            connection.close()  # Fechar a conexão com o banco
            return df
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None
        except Exception as e:
            print(f"Erro ao carregar dados do banco: {e}")
            return None

def load_csv_data(filename):
    """
    Função para carregar dados CSV em paralelo.
    """
    data_loader_csv = DataLoader(source_type='csv', source_path='data')
    df = data_loader_csv.load(filename)
    return df

def load_db_data(table_name):
    """
    Função para carregar dados de banco de dados em paralelo.
    """
    data_loader_db = DataLoader(source_type='db', source_path='public')
    df = data_loader_db.load(table_name)
    return df
