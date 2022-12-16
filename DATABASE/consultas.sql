-- Consulta que retorna valor booleano indicando se o filme já consta no banco ou não, a partir do imdb_id
SELECT EXISTS (SELECT 1 FROM filme WHERE imdb_id='{filme['imdbID']}');

-- Consulta que retorna os filmes em ordem decrescnete de datahora
SELECT imdb_id, titulo, ano, duracao_min, genero, nota_imdb, poster, datahora
       FROM filme
       ORDER BY datahora DESC;
