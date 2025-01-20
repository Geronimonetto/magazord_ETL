import os
import pandas as pd
import duckdb
from pathlib import Path
import psycopg2


# Caminho do projeto na maquina atual
base_path = Path(__file__).parent if '__file__' in globals() else Path.cwd()
data_path = base_path.parent / 'data' / 'staged'

class DataLoader:
    def __init__(self, source_type: str, source_path: str):
        """
        Inicializa o DataLoader.
        :param source_type: Tipo de fonte de dados ('csv' ou 'db').
        :param source_path: Caminho para os dados. Para 'csv' é o diretório, 
                            para 'db' é o nome do banco de dados ou schema.
        """
        self.source_type = source_type
        self.source_path = source_path

    def load(self, table_name: str):
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

    def _load_from_csv(self, table_name: str) -> pd.DataFrame:
        """
        Carregar dados a partir de arquivos CSV usando DuckDB.
        Se o caminho for uma pasta, ele lê todos os CSVs na pasta.
        :param table_name: Nome do arquivo ou pasta que contém os CSVs.
        :return: DataFrame com os dados carregados.
        """
        try:
            # Verifica se é uma pasta ou arquivo
            path = data_path / table_name
            print(f"Caminho do arquivo/pasta: {path}")
            
            if path.is_dir():  # Se for uma pasta
                dfs = []  # Lista para armazenar os DataFrames de todos os CSVs na pasta
                for csv_file in os.listdir(path):
                    if csv_file.endswith('.csv'):  # Só considera arquivos CSV
                        file_path = path / csv_file
                        print(f"Lendo arquivo CSV: {file_path}")
                        with duckdb.connect() as con:
                            df = con.execute(f"SELECT * FROM read_csv_auto('{file_path}')").fetchdf()
                            dfs.append(df)
                # Concatenar todos os DataFrames dos arquivos CSV encontrados
                if dfs:
                    return pd.concat(dfs, ignore_index=True)
                else:
                    print(f"Nenhum arquivo CSV encontrado na pasta {path}.")
                    return None
            else:
                # Se for um único arquivo CSV
                if not path.exists():
                    raise FileNotFoundError(f"O arquivo {path} não foi encontrado.")
                with duckdb.connect() as con:
                    df = con.execute(f"SELECT * FROM read_csv_auto('{path}')").fetchdf()
                    return df
        except FileNotFoundError as e:
            print(f"Erro: {e}")
            return None
        except Exception as e:
            print(f"Erro ao carregar o CSV: {e}")
            return None

    def _load_from_db(self, table_name: str) -> pd.DataFrame:
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

def load_csv_data(filename: str) -> object:
    """
    Função para carregar dados CSV em paralelo.
    """
    data_loader_csv = DataLoader(source_type='csv', source_path='data')
    df = data_loader_csv.load(filename)
    return df

def load_db_data(table_name: str):
    """
    Função para carregar dados de banco de dados em paralelo.
    """
    data_loader_db = DataLoader(source_type='db', source_path='public')
    df = data_loader_db.load(table_name)
    return df

