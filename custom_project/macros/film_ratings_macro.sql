{% macro generate_film_ratings() %}

-- depends_on: {{ ref('stg_films') }}
-- depends_on: {{ ref('stg_film_actors') }}
-- depends_on: {{ ref('stg_actors') }}
WITH films_with_ratings AS (
    SELECT
        film_id,
        title,
        release_date,
        price,
        rating,
        user_rating,
        CASE
            WHEN user_rating >= 4.5 THEN 'Excellent'
            WHEN user_rating >= 4.0 THEN 'Good'
            WHEN user_rating >= 3.0 THEN 'Average'
            ELSE 'Poor'
        END AS rating_category
    FROM
        {{ ref('stg_films') }}
),
films_with_actors AS (
    SELECT
        f.film_id,
        f.title,
        STRING_AGG(a.actor_name, ', ') AS actors
    FROM
        {{ ref('stg_films') }} f
        LEFT JOIN {{ ref('stg_film_actors') }} fa ON f.film_id = fa.film_id
        LEFT JOIN {{ ref('stg_actors') }} a ON fa.actor_id = a.actor_id
    GROUP BY
        f.film_id,
        f.title
)
SELECT
    fwf.*,
    fwa.actors
FROM
    films_with_ratings fwf
    LEFT JOIN films_with_actors fwa ON fwf.film_id = fwa.film_id

{% endmacro %}