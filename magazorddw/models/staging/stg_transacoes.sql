-- import
with source as (
    select
        "id_transacao",
        "id_cliente",
        "id_produto",
        "quantidade",
        "data_transacao"
    from 
        {{ source ('production' , 'transacoes')}}

),
-- renamed

renamed as (
    SELECT
        "id_transacao" as id_transacao,
        cast("data_transacao" as date) as data_transacao,
        "id_cliente" as id_cliente,
        "id_produto" as id_produto,
        "quantidade" as quantidade
    FROM
        source
)

SELECT * FROM renamed