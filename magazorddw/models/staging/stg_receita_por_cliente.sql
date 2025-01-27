-- Receita total por cliente
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

-- Junta com a tabela de produtos para obter o preço
with_prices as (
    select
        r.id_cliente,
        r.id_produto,
        r.quantidade,
        p.preco,
        r.quantidade * p.preco as receita
    from
        renamed r
    left join 
        {{ source('production', 'produtos') }} p
    on
        r.id_produto = p.id_produto
),

-- Soma a receita por cliente
receita_por_cliente as (
    select
        id_cliente,
        sum(receita) as receita_total
    from
        with_prices
    group by
        id_cliente
)

select * from receita_por_cliente
