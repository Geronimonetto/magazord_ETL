WITH clientes_ativos AS (
    SELECT 
        "id_cliente", 
        COUNT("id_transacao") AS total_transacoes
    FROM 
        {{ ref('stg_transacoes') }} 
    WHERE 
        "data_transacao" >= current_date - interval '3 months'
    GROUP BY 
        "id_cliente"
)
SELECT 
    COUNT(*) AS numero_clientes_ativos
FROM 
    clientes_ativos
WHERE 
    total_transacoes > 0
