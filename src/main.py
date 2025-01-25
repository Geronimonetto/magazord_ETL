from concurrent.futures import ThreadPoolExecutor
from utils.connection import load_csv_data, load_db_data
from utils.create_tables import execute_sql_file, insert_into_table
from utils.transform_data import transformar_csv_cliente, transformar_csv_produto, transformar_csv_transacao

output_parquet_cliente = './data/raw/cliente.parquet'
output_parquet_produto = './data/raw/produto.parquet'
output_parquet_transacao = './data/raw/transacoes.parquet'


def run():
    # Arquivos CSV e tabelas do banco de dados a serem lidos
    csv_files = ['cliente.csv', 'produtos.csv', 'transacoes']
    db_tables = ['clientes', 'produtos', 'transacoes']

    # Usando multiprocessing com ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        
        # Carregar dados CSV e DB em paralelo
        csv_results = list(executor.map(load_csv_data, csv_files))
        db_results = list(executor.map(load_db_data, db_tables))
        
    # Desempacotar os resultados
    clientes_df_csv, produtos_df_csv, transacoes_df_csv = csv_results
    clientes_df_db, produtos_df_db, transacoes_df_db = db_results

    # Transformar os dados e salvar em Parquet
    transformar_csv_cliente(clientes_df_csv, output_parquet_cliente) 
    transformar_csv_produto(produtos_df_csv, output_parquet_produto)  
    transformar_csv_transacao(transacoes_df_csv, output_parquet_transacao)

    # Inserir os dados transformados no banco de dados
    insert_into_table(clientes_df_csv, "clientes")  # Nome da tabela no banco
    insert_into_table(produtos_df_csv, "produtos")  # Nome da tabela no banco
    insert_into_table(transacoes_df_csv, "transacoes")  # Nome da tabela no banco



if __name__ == "__main__":
    # Caminho do arquivo .sql
    sql_file_path = "./scripts/create_tables.sql"
    
    # Executar os comandos SQL do arquivo
    execute_sql_file(sql_file_path)
    run()
