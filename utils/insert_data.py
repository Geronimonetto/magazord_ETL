import psycopg2
import os
# Conectar ao banco de dados PostgreSQL
connection = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

# Criar um cursor para executar o comando
cursor = connection.cursor()

# Caminho para o arquivo CSV
csv_file_path = '/caminho/para/o/arquivo/clientes.csv'

# Comando COPY para inserir os dados
copy_query = f"""
COPY clientes (id, nome, idade)
FROM '{csv_file_path}'
DELIMITER ','
CSV HEADER;
"""

try:
    # Executar o comando COPY
    cursor.execute(copy_query)
    connection.commit()  # Commit para garantir que os dados foram inseridos
    print("Dados inseridos com sucesso!")
except Exception as e:
    print(f"Erro ao inserir dados: {e}")
    connection.rollback()  # Caso ocorra um erro, faz rollback
finally:
    # Fechar a conexão
    cursor.close()
    connection.close()
