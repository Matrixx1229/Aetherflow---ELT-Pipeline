{% set film_title = 'Dunkirk' %}

select *
from {{ref('stg_films')}}
where title = '{{ film_title }}'