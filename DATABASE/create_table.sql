-- Criando tabela principal 'filme'

CREATE TABLE filme (
	imdb_id varchar(15),
	titulo varchar(250) NOT NULL,
	ano int NOT NULL,
	duracao_min int,
	nota_imdb decimal(2,1),
	genero varchar(250),
	sinopse varchar(1000),
	escrito_por varchar(250),
	atores varchar(250),
	idioma varchar(250),
	pais varchar(250),
	premios varchar(500),
	poster varchar(1000),
	datahora timestamp default CURRENT_TIMESTAMP(2) NOT NULL,

	Constraint PK_IMDB_ID Primary Key(imdb_id)
);