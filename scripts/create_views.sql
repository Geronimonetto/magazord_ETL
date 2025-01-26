-- View: Receita Total por Cliente
CREATE OR REPLACE VIEW receita_total_por_cliente AS
SELECT 
    t.id_cliente,
    c.nome_cliente AS nome_cliente,
    SUM(t.quantidade * p.preco) AS receita_total
FROM 
    public.transacoes t 
JOIN 
    public.produtos p ON t.id_produto = p.id_produto
JOIN 
    public.clientes c ON t.id_cliente = c.id_cliente
GROUP BY 
    t.id_cliente, c.nome_cliente;

-- View: Número Total de Transações por Cliente
CREATE OR REPLACE VIEW numero_total_transacoes_por_cliente AS
SELECT 
    t.id_cliente,
    c.nome_cliente AS nome_cliente,
    COUNT(*) AS numero_transacoes
FROM 
    public.transacoes t
JOIN 
    public.clientes c ON t.id_cliente = c.id_cliente
GROUP BY 
    t.id_cliente, c.nome_cliente;

-- View: Produto Mais Comprado por Cliente
CREATE OR REPLACE VIEW produto_mais_comprado_por_cliente AS
SELECT 
    t.id_cliente,
    c.nome_cliente AS nome_cliente,
    t.id_produto,
    p.nome_produto,
    SUM(t.quantidade) AS quantidade
FROM 
    public.transacoes t
JOIN 
    public.produtos p ON t.id_produto = p.id_produto
JOIN 
    public.clientes c ON t.id_cliente = c.id_cliente
GROUP BY 
    t.id_cliente, c.nome_cliente, t.id_produto, p.nome_produto
ORDER BY 
    quantidade DESC;
