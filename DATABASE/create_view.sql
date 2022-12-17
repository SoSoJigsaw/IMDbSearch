--Criando a view do route "mostrar_filmes"
CREATE VIEW mostrar_filmes_view AS
SELECT f.imdb_id, f.titulo, f.ano, f.duracao_min,
CONCAT(g.genero_1, ' ', g.genero_2, ' ', g.genero_3, ' ',
				 g.genero_4, ' ', g.genero_5, ' ',
				 g.genero_6, ' ', g.genero_7, ' ', g.genero_8, ' ',
				 g.genero_9, ' ', g.genero_10) AS genero,
f.nota_imdb, f.poster, f.datahora
FROM filme f, genero g
WHERE f.imdb_id=g.imdb_id
ORDER BY datahora DESC;


--Criando a view do route "mostrar_detalhes_filme"
CREATE VIEW mostrar_detalhes_filme_view AS
SELECT f.imdb_id, f.titulo, f.ano, f.duracao_min, f.nota_imdb,
CONCAT(g.genero_1, ' ', g.genero_2, ' ', g.genero_3, ' ',
				 g.genero_4, ' ', g.genero_5, ' ',
				 g.genero_6, ' ', g.genero_7, ' ', g.genero_8, ' ',
				 g.genero_9, ' ', g.genero_10) AS genero,
f.sinopse, f.escrito_por, f.atores, f.idioma, f.pais, f.premios, f.poster
FROM filme f, genero g
WHERE f.imdb_id=g.imdb_id;