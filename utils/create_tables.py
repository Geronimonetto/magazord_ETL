import psycopg2
import os
from dotenv import load_dotenv

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

# Exemplo de uso do script
if __name__ == "__main__":
    # Caminho do arquivo .sql
    sql_file_path = "./scripts/create_tables.sql"
    
    # Executar os comandos SQL do arquivo
    execute_sql_file(sql_file_path)
