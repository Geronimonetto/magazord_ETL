WITH receita_por_categoria AS (
    SELECT 
        p.categoria,
        SUM(t.quantidade * p.preco) AS receita_total
    FROM 
        {{ ref('stg_transacoes') }} t
    JOIN 
        {{ ref('stg_produtos') }} p
        ON t.id_produto = p.id_produto
    GROUP BY 
        p.categoria
)
SELECT 
    categoria, 
    receita_total
FROM 
    receita_por_categoria
