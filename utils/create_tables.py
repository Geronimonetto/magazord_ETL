import psycopg2
import duckdb
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import time
# Carregar as variáveis de ambiente do arquivo .env (caso esteja usando)
load_dotenv()

# Função para conectar ao banco de dados
def connect_to_db():
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

# Função para executar os comandos SQL contidos no arquivo
def execute_sql_file(file_path):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Abrir o arquivo .sql
            with open(file_path, 'r') as sql_file:
                sql_commands = sql_file.read()

            # Executar os comandos SQL
            cursor.execute(sql_commands)
            conn.commit()
            print(f"Tabelas criadas com sucesso a partir de {file_path}.")
        except Exception as e:
            print(f"Erro ao executar os comandos SQL: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def insert_into_table(df, table_name):
    try:
        star_time = time.time()
        # Criar engine de conexão com o banco de dados
        engine = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
        
        # Inserir os dados diretamente no banco usando pandas
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Dados inseridos com sucesso na tabela {table_name}.")
        end_time = time.time() - star_time
        print(f"Tempo de execução: {end_time} segundos.")
    except Exception as e:
        print(f"Erro ao inserir dados na tabela {table_name}: {e}")

