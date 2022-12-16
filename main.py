import json
from sqlalchemy import create_engine
import requests
from flask import Flask, render_template, request, jsonify, flash, redirect

app = Flask(__name__)
app.secret_key = '1234'
db = create_engine('postgresql://postgres:123@[localhost]/Filmes')


@app.route("/")
def pesquisa():

    return render_template("index.html")


@app.route("/resultado/<string:imdbID>", methods=['GET'])
def resultado(imdbID):

    data_URL = f"http://www.omdbapi.com/?i={imdbID}&apikey=b0202a42"

    filme = requests.get(data_URL).json()

    filme['Year'] = filme['Year'].replace('–', '')

    filme['Plot'] = filme['Plot'].replace("'", "`")
    filme['Title'] = filme['Title'].replace("'", "`")
    filme['Awards'] = filme['Awards'].replace("'", "`")

    filme['Poster'] = filme['Poster'].replace('N/A', '/static/image/sem_imagem.gif')

    existe_no_banco = db.execute(f"SELECT EXISTS (SELECT 1 FROM filme WHERE imdb_id='{filme['imdbID']}')").scalar()

    return render_template('resultado.html', filme=filme, existe_no_banco=existe_no_banco)


@app.route("/salvar/<string:imdbID>", methods=['GET'])
def salvar_filme(imdbID):

    try:

        data_URL = f"http://www.omdbapi.com/?i={imdbID}&apikey=b0202a42"

        filme = requests.get(data_URL).json()

        filme['Year'] = filme['Year'].replace('–', '')

        filme['Runtime'] = filme['Runtime'].replace(' min', '')
        filme['Runtime'] = filme['Runtime'].replace('N/A', 'NULL')

        filme['imdbRating'] = filme['imdbRating'].replace('N/A', 'NULL')

        filme['Plot'] = filme['Plot'].replace("'", "`")
        filme['Title'] = filme['Title'].replace("'", "`")
        filme['Awards'] = filme['Awards'].replace("'", "`")

        filme['Poster'] = filme['Poster'].replace('N/A', '/static/image/sem_imagem.gif')

        db.execute(f"INSERT INTO filme (imdb_id, titulo, ano, duracao_min, nota_imdb, genero, sinopse, escrito_por, atores, "
                   f"idioma, pais, premios, poster) VALUES ('{filme['imdbID']}', '{filme['Title']}', {filme['Year']}, "
                   f"{filme['Runtime']}, {filme['imdbRating']}, '{filme['Genre']}', '{filme['Plot']}', "
                   f"'{filme['Writer']}', '{filme['Actors']}', '{filme['Language']}', '{filme['Country']}', "
                   f"'{filme['Awards']}', '{filme['Poster']}')")

        print(f"'{filme['Title']}' adicionado à lista de filmes do usuário")

    except:
        pass

    return redirect('/filmes')


@app.route("/remover/<string:imdbID>", methods=['GET'])
def apagar_filme(imdbID):

    try:

        db.execute(f"DELETE FROM filme WHERE imdb_id= '{imdbID}';")

    except:
        pass

    return redirect('/filmes')


@app.route("/filmes", methods=['GET'])
def mostrar_filmes():

    query = db.execute("SELECT imdb_id, titulo, ano, duracao_min, genero, nota_imdb, poster, datahora FROM filme "
                       "ORDER BY datahora DESC;").fetchall()

    return render_template('minhalista.html', query=query)


@app.route("/filmes/<string:imdbID>", methods=['GET'])
def mostrar_detalhes_filme(imdbID):

    query = db.execute(f"SELECT * FROM filme WHERE imdb_id = '{imdbID}'").fetchall()

    existe_no_banco = db.execute(f"SELECT EXISTS (SELECT 1 FROM filme WHERE imdb_id='{imdbID}')").scalar()

    return render_template('detalhes.html', query=query, existe_no_banco=existe_no_banco)


if __name__ == "__main__":
    app.run(debug=True)