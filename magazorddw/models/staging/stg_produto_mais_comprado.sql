-- Produto mais comprado por cliente
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

quantidade_por_produto as (
    select
        id_cliente,
        id_produto,
        sum(quantidade) as total_quantidade
    from
        renamed
    group by
        id_cliente, id_produto
),

produto_mais_comprado as (
    select
        id_cliente,
        id_produto,
        total_quantidade
    from (
        select
            id_cliente,
            id_produto,
            total_quantidade,
            row_number() over (partition by id_cliente order by total_quantidade desc) as rank
        from
            quantidade_por_produto
    ) ranked
    where
        rank = 1
)

select * from produto_mais_comprado
