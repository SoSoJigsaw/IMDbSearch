-- Criando tabela principal 'filme'
CREATE TABLE filme (
	imdb_id varchar(15),
	titulo varchar(250) NOT NULL,
	ano int NOT NULL,
	duracao_min int,
	nota_imdb decimal(2,1),
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


--Criando tabela do 'genero'
CREATE TABLE genero (
	imdb_id varchar(15),
	genero_1 varchar(40),
	genero_2 varchar(40),
	genero_3 varchar(40),
	genero_4 varchar(40),
	genero_5 varchar(40),
	genero_6 varchar(40),
	genero_7 varchar(40),
	genero_8 varchar(40),
	genero_9 varchar(40),
	genero_10 varchar(40),

	Constraint PK_GENERO Primary Key(imdb_id),
	Constraint FK_GENERO_IMDB_ID Foreign Key(imdb_id) REFERENCES filme(imdb_id)
);
