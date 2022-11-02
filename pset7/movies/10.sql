SELECT name from people
JOIN directors ON directors.person_id = people.id
JOIN movies ON movies.id  = directors.movie_id
JOIN ratings on ratings.movie_id = movies.id
WHERE rating >= 9;