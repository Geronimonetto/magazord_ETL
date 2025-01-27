import time
from utils.connection import load_csv_data, load_db_data
from utils.create_tables import execute_sql_file, insert_into_table
from utils.transform_data import transformar_csv_cliente, transformar_csv_produto, transformar_csv_transacao
from concurrent.futures import ThreadPoolExecutor

# Caminhos dos arquivos Parquet de saída
output_parquet_cliente = './data/raw/cliente.parquet'
output_parquet_produto = './data/raw/produto.parquet'
output_parquet_transacao = './data/raw/transacoes.parquet'

# Função para carregar e transformar os dados
def load_and_transform_data():
    print("Iniciando carregamento e transformação de dados...")

    # Arquivos CSV a serem lidos
    csv_files = ['cliente.csv', 'produtos.csv', 'transacoes']

    # Usando ThreadPoolExecutor para carregar dados CSV em paralelo
    with ThreadPoolExecutor() as executor:
        csv_results = list(executor.map(load_csv_data, csv_files))

    # Desempacotar os resultados
    clientes_df_csv, produtos_df_csv, transacoes_df_csv = csv_results

    # Transformar os dados e salvar em Parquet
    transformar_csv_cliente(clientes_df_csv, output_parquet_cliente)
    transformar_csv_produto(produtos_df_csv, output_parquet_produto)
    transformar_csv_transacao(transacoes_df_csv, output_parquet_transacao)

    print("Dados transformados com sucesso!")
    return clientes_df_csv, produtos_df_csv, transacoes_df_csv

# Função para processar e inserir os dados no banco
def process_and_insert_data():
    print("Iniciando inserção de dados no banco de dados...")

    # Carregar os dados transformados
    clientes_df_csv, produtos_df_csv, transacoes_df_csv = load_and_transform_data()

    # Verificar se os 'id_cliente' nas transações existem na tabela de clientes
    clientes_ids = set(clientes_df_csv['id_cliente'])  # Extrair os IDs de clientes válidos

    # Substituir 'id_cliente' por None (NULL) nas transações caso não seja encontrado
    transacoes_df_csv['id_cliente'] = transacoes_df_csv['id_cliente'].apply(
        lambda x: x if x in clientes_ids else None
    )

    # Inserir os dados no banco de dados em ordem sequencial
    insert_into_table(clientes_df_csv, "clientes")  # Inserir dados de clientes primeiro
    insert_into_table(produtos_df_csv, "produtos")  # Inserir dados de produtos depois
    insert_into_table(transacoes_df_csv, "transacoes")  # Inserir dados de transações por último

    print("Dados inseridos no banco de dados com sucesso!")


# Função principal que executa as tarefas sequenciais
def run():
    start_time = time.time()

    print("Iniciando o fluxo de trabalho...")

    # Passo 1: Criar as tabelas (executar o arquivo SQL)
    print("Criando tabelas no banco de dados...")
    sql_file_path = "./scripts/create_tables.sql"
    execute_sql_file(sql_file_path)
    print("Tabelas criadas com sucesso!")

    # Passo 2: Processar e inserir os dados
    process_and_insert_data()

    # Finalizando o fluxo
    end_time = time.time() - start_time
    print(f"Fluxo de trabalho concluído em {end_time:.2f} segundos.")

if __name__ == "__main__":
    run()
