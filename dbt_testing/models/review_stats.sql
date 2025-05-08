SELECT
    m.movie_title,
    COUNT(ur.review_id) AS user_review_count,
    COUNT(cr.review_id) AS critic_review_count,
    AVG(ur.score) AS avg_user_score,
    AVG(
    CASE
        WHEN cr.original_score LIKE '%/%'
        THEN SPLIT_PART(cr.original_score, '/', 1)::float / NULLIF(SPLIT_PART(cr.original_score, '/', 2)::float, 0)
        ELSE cr.original_score::float
    END
) AS avg_critic_score


FROM {{ ref('movies') }} m
LEFT JOIN {{ ref('user_reviews') }} ur ON ur.movie_id = m.movie_id
LEFT JOIN {{ ref('critic_reviews') }} cr ON cr.movie_id = m.movie_id
GROUP BY m.movie_title