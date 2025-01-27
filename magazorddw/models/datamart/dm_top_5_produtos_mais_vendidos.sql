WITH top_produtos AS (
    SELECT 
        p.id_produto, 
        p.nome_produto, 
        SUM(t.quantidade) AS quantidade_total
    FROM 
        {{ ref('stg_transacoes') }} t
    JOIN 
        {{ ref('stg_produtos') }} p
        ON t.id_produto = p.id_produto
    GROUP BY 
        p.id_produto, p.nome_produto
    ORDER BY 
        quantidade_total DESC
    LIMIT 5
)
SELECT 
    id_produto,
    nome_produto,
    quantidade_total
FROM 
    top_produtos
