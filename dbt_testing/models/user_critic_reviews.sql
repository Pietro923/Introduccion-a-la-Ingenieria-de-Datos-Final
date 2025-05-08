SELECT
    ur.user_id,
    ur.movie_id,
    ur.score AS user_score,
    cr.original_score AS critic_score,
    m.movie_title
FROM {{ ref('user_reviews') }} ur
JOIN {{ ref('critic_reviews') }} cr ON ur.movie_id = cr.movie_id
JOIN {{ ref('movies') }} m ON m.movie_id = ur.movie_id
