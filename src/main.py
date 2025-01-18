from utils.connection import DataLoader

if __name__ == "__main__":
    # Carregar dados de CSV
    data_loader_csv = DataLoader(source_type='csv', source_path='data')  # Ajustando o caminho para 'data' que está fora de src
    clientes_df_csv = data_loader_csv.load('cliente.csv')
    produtos_df_csv = data_loader_csv.load('produtos.csv')
    
    # Carregar dados de Banco de Dados
    data_loader_db = DataLoader(source_type='db', source_path='public')  # Passando 'public' como schema para o banco
    clientes_df_db = data_loader_db.load('clientes')
    produtos_df_db = data_loader_db.load('produtos')
    
    # Exemplo de uso
    print(clientes_df_csv.head())  # Exibindo os dados carregados de 'cliente.csv'
    print(produtos_df_csv.head())  # Exibindo os dados carregados de 'produtos.csv'
    print(clientes_df_db.head())   # Exibindo os dados carregados de 'cliente' do banco
    print(produtos_df_db.head())   # Exibindo os dados carregados de 'produtos' do banco