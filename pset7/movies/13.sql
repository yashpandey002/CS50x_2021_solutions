SELECT name FROM people WHERE id IN
(SELECT person_id FROM stars WHERE movie_id IN
(SELECT movies.id FROM people
JOIN stars ON stars.person_id = people.id
JOIN movies ON movies.id = stars.movie_id
WHERE people.name = "Kevin Bacon"
AND people.birth = 1958) AND people.name != "Kevin Bacon");