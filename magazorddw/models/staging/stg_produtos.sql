-- import
with source as (
    select
        "id_produto",
        "nome_produto",
        "categoria",
        "preco"
    from 
        {{ source ('production' , 'produtos')}}

),
-- renamed

renamed as (
    SELECT
        "id_produto" as id_produto,
        "nome_produto" as nome_produto,
        "categoria" as categoria,
        "preco" as preco
    FROM
        source
)

SELECT * FROM renamed