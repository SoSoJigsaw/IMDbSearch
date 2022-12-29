from sqlalchemy import create_engine


# Função que retorna uma lista dos gêneros disponíveis no banco de dados, para serem usados como opções no field
# "genero"
def genero_options():

    # Conexão com o banco
    db = create_engine('postgresql://postgres:123@[localhost]/Filmes')

    # Query que retorna todos os gêneros disponíveis no banco de daods
    query = db.execute("SELECT DISTINCT genero_1, genero_2, genero_3, genero_4, genero_5, genero_6, "
                       "genero_7, genero_8, genero_9, genero_10 FROM genero").fetchall()

    # For loop que transforma a query de um objeto sql em uma lista python com todos os valores originais da query
    generos = []
    for q in query:
        for x in q:
            if x is not None:
                generos.append(x)

    # Retirando as duplicadas da lista
    generos = list(dict.fromkeys(generos))

    return generos