from concurrent.futures import ThreadPoolExecutor
from utils.connection import load_csv_data, load_db_data
def main():
    # Definir arquivos e tabelas para carregar
    csv_files = ['cliente.csv', 'produtos.csv']
    db_tables = ['clientes', 'produtos']

    # Usando multiprocessing com ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        # Carregar CSV e DB em paralelo
        csv_results = list(executor.map(load_csv_data, csv_files))
        db_results = list(executor.map(load_db_data, db_tables))
        
    # Desempacotar os resultados
    clientes_df_csv, produtos_df_csv = csv_results
    clientes_df_db, produtos_df_db = db_results

    # Exemplo de uso
    print(clientes_df_csv.head())  # Exibindo os dados carregados de 'cliente.csv'
    print(produtos_df_csv.head())  # Exibindo os dados carregados de 'produtos.csv'
    print(clientes_df_db.head())   # Exibindo os dados carregados de 'cliente' do banco
    print(produtos_df_db.head())   # Exibindo os dados carregados de 'produtos' do banco

if __name__ == "__main__":
    main()