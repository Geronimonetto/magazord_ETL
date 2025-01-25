-- Remover tabelas caso já existam
DROP TABLE IF EXISTS transacoes;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS clientes;

-- Criação da tabela de clientes
CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    nome_cliente VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(15)
);

-- Criação da tabela de produtos
CREATE TABLE produtos (
    id_produto INT PRIMARY KEY,
    nome_produto VARCHAR(100),
    categoria VARCHAR(50),
    preco DECIMAL(10, 2)
);

-- Criação da tabela de transações
CREATE TABLE transacoes (
    id_transacao INT PRIMARY KEY,
    id_cliente INT REFERENCES clientes(id_cliente),
    id_produto INT REFERENCES produtos(id_produto),
    quantidade INT,
    data_transacao DATE
);
