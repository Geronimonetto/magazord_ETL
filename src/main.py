from concurrent.futures import ThreadPoolExecutor
from utils.connection import load_csv_data, load_db_data


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

    # Exibir as primeiras linhas de cada DataFrame carregado
    print("CSV - Cliente:")
    print(clientes_df_csv.head()) 
    print("CSV - Produtos:")
    print(produtos_df_csv.head())  
    print("CSV - Transações:")
    print(transacoes_df_csv.head())

    print("DB - Cliente:")
    print(clientes_df_db.head())  
    print("DB - Produtos:")
    print(produtos_df_db.head())  
    print("DB - Transações:")
    print(transacoes_df_db.head())   

if __name__ == "__main__":
    run()
