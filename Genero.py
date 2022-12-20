from sqlalchemy import create_engine


def genero_options():

    db = create_engine('postgresql://postgres:123@[localhost]/Filmes')

    query = db.execute("SELECT DISTINCT genero_1, genero_2, genero_3, genero_4, genero_5, genero_6, "
                       "genero_7, genero_8, genero_9, genero_10 FROM genero").fetchall()

    generos = []
    for q in query:
        for x in q:
            if x is not None:
                generos.append(x)

    generos = list(dict.fromkeys(generos))

    return generos