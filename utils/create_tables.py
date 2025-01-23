import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Função para conectar ao banco de dados usando psycopg2
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

# Função para executar comandos SQL de um arquivo
def execute_sql_file(file_path):
    conn = connect_to_db()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            with open(file_path, 'r') as sql_file:
                sql_commands = sql_file.read()
            cursor.execute(sql_commands)
            conn.commit()
            print(f"Tabelas criadas com sucesso a partir de {file_path}.")
    except Exception as e:
        print(f"Erro ao executar os comandos SQL: {e}")
        conn.rollback()
    finally:
        conn.close()

# Função para inserir dados de um DataFrame no banco de dados
def insert_into_table(df, table_name):
    try:
        # Criar engine de conexão com SQLAlchemy
        engine = create_engine(
            f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@'
            f'{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
        )
        # Usar pandas para inserir os dados
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Dados inseridos com sucesso na tabela {table_name}.")
    except Exception as e:
        print(f"Erro ao inserir dados na tabela {table_name}: {e}")
