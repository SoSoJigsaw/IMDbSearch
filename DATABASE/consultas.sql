-- Consulta que retorna valor booleano indicando se o filme já consta no banco ou não, a partir do imdb_id
SELECT EXISTS (SELECT 1 FROM filme WHERE imdb_id='{filme['imdbID']}');

-- Consulta que retorna os filmes em ordem decrescnete de datahora
SELECT imdb_id, titulo, ano, duracao_min, genero, nota_imdb, poster, datahora
       FROM filme
       ORDER BY datahora DESC;


--Consulta que possibilita um array de valores para a cláusula LIKE
SELECT * FROM genero WHERE genero_1 LIKE ANY (array['%Adventure%', '%Family%']);


--Consulta que possibilita a demonstação da view e ao mesmo tempo a comparação com os gêneros dos filmes, por junção
SELECT * FROM mostrar_filmes_view v, genero g WHERE v.imdb_id=g.imdb_id AND g.genero_1 LIKE '%Adventure%'

--Consulta completa da pesquisa do site, com arrays nos gêneros para escolha de múltiplos gêneros
SELECT * FROM mostrar_filmes_view v, genero g WHERE v.imdb_id=g.imdb_id
AND v.ano >= 1990 AND v.ano <= 2015 AND v.duracao_min >= 25
AND v.duracao_min <= 150 AND v.nota_imdb >= 5.5 AND v.nota_imdb <= 9
AND (g.genero_1 = ANY (array['Adventure', 'Family'])
	 OR g.genero_2 = ANY (array['Adventure', 'Family'])
	 OR g.genero_3 = ANY (array['Adventure', 'Family'])
	 OR g.genero_4 = ANY (array['Adventure', 'Family'])
	 OR g.genero_5 = ANY (array['Adventure', 'Family'])
	 OR g.genero_6 = ANY (array['Adventure', 'Family'])
	 OR g.genero_7 = ANY (array['Adventure', 'Family'])
	 OR g.genero_8 = ANY (array['Adventure', 'Family'])
	 OR g.genero_9 = ANY (array['Adventure', 'Family'])
	 OR g.genero_10 = ANY (array['Adventure', 'Family']));