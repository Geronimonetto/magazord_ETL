-- Número total de transações por cliente
with source as (
    select
        "id_transacao",
        "id_cliente",
        "id_produto",
        "quantidade",
        "data_transacao"
    from 
        {{ source('production', 'transacoes') }}
),

renamed as (
    select
        "id_transacao" as id_transacao,
        cast("data_transacao" as date) as data_transacao,
        "id_cliente" as id_cliente,
        "id_produto" as id_produto,
        "quantidade" as quantidade
    from
        source
),

-- Conta o número de transações por cliente
transacoes_por_cliente as (
    select
        id_cliente,
        count(id_transacao) as total_transacoes
    from
        renamed
    group by
        id_cliente
)

select * from transacoes_por_cliente
