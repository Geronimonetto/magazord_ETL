-- import
with source as (
    select
        "id_cliente",
        "nome_cliente",
        "email",
        "telefone"
    from 
        {{ source ('production' , 'clientes')}}

),
-- renamed

renamed as (
    SELECT
        "id_cliente" as id_cliente,
        "nome_cliente" as nome_cliente,
        "email" as email,
        "telefone" as telefone
    FROM
        source
)

SELECT * FROM renamed