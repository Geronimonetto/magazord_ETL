WITH transacoes_aggregadas AS (
    SELECT
        t.id_cliente,
        t.id_produto,
        SUM(t.quantidade) AS total_quantidade,
        SUM(t.quantidade * p.preco) AS total_receita
    FROM {{ ref('stg_transacoes') }} t
    JOIN {{ ref('stg_produtos') }} p ON t.id_produto = p.id_produto
    GROUP BY t.id_cliente, t.id_produto
)

SELECT
    c.id_cliente,
    c.nome_cliente,
    c.email,
    c.telefone,
    ta.id_produto,
    p.nome_produto,
    p.categoria,
    ta.total_quantidade,
    ta.total_receita
FROM transacoes_aggregadas ta
JOIN {{ ref('stg_clientes') }} c ON ta.id_cliente = c.id_cliente
JOIN {{ ref('stg_produtos') }} p ON ta.id_produto = p.id_produto
