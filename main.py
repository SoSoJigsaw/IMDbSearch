import json
import random
from sqlalchemy import create_engine
import requests
from flask import Flask, render_template, request, jsonify, flash, redirect
from forms import ConsultaForm

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

        db.execute(f"INSERT INTO filme (imdb_id, titulo, ano, duracao_min, nota_imdb, sinopse, escrito_por, atores, "
                   f"idioma, pais, premios, poster) VALUES ('{filme['imdbID']}', '{filme['Title']}', {filme['Year']}, "
                   f"{filme['Runtime']}, {filme['imdbRating']}, '{filme['Plot']}', "
                   f"'{filme['Writer']}', '{filme['Actors']}', '{filme['Language']}', '{filme['Country']}', "
                   f"'{filme['Awards']}', '{filme['Poster']}')")

        print(f"'{filme['Title']}' adicionado à lista de filmes do usuário")

        i = 0
        genre_string = filme['Genre']
        genre = []
        while i <= genre_string.count(','):
            if genre_string.count(',') == 0:
                genre.append(genre_string)
            else:
                genre.append(genre_string.split(",", genre_string.count(','))[i])
                i += 1

        i = 0
        while i <= len(genre) - 1:
            genre[i] = genre[i].replace(' ', '')
            i += 1

        db.execute(f"INSERT INTO genero VALUES ('{filme['imdbID']}', {str(genre)[1:-1]})")

    except:
        raise

    return redirect('/filmes')


@app.route("/remover/<string:imdbID>", methods=['GET'])
def apagar_filme(imdbID):

    try:

        db.execute(f"DELETE FROM genero WHERE imdb_id= '{imdbID}';")

        db.execute(f"DELETE FROM filme WHERE imdb_id= '{imdbID}';")

    except:
        raise

    return redirect('/filmes')


@app.route("/filmes", methods=['GET'])
def mostrar_filmes():

    form = ConsultaForm()

    query = db.execute("SELECT * FROM mostrar_filmes_view;").fetchall()

    return render_template('minhalista.html', query=query, form=form)


@app.route("/filmes", methods=['POST'])
def mostrar_filmes_post():

    form = ConsultaForm()

    if form.validate_on_submit():
        if form.anoMin.data == '':
            formAnoMin = ''
        else:
            formAnoMin = f" AND v.ano >= {form.anoMin.data}"

        if form.anoMax.data == '':
            formAnoMax = ''
        else:
            formAnoMax = f" AND v.ano <= {form.anoMax.data}"

        if form.duracaoMin.data == '':
            formDuracaoMin = ''
        else:
            formDuracaoMin = f" AND v.duracao_min >= {form.duracaoMin.data}"

        if form.duracaoMax.data == '':
            formDuracaoMax = ''
        else:
            formDuracaoMax = f" AND v.duracao_min <= {form.duracaoMax.data}"

        if form.notaMin.data == '':
            formNotaMin = ''
        else:
            formNotaMin = f" AND v.nota_imdb >= {form.notaMin.data}"

        if form.notaMax.data == '':
            formNotaMax = ''
        else:
            formNotaMax = f" AND v.nota_imdb <= {form.notaMax.data}"

        if not form.genero.data:
            formGenero = ''
        else:
            formGenero = f" AND (g.genero_1 = ANY (array{form.genero.data}) " \
                         f"OR g.genero_2 = ANY (array{form.genero.data}) " \
                         f"OR g.genero_3 = ANY (array{form.genero.data}) " \
                         f"OR g.genero_4 = ANY (array{form.genero.data}) " \
                         f"OR g.genero_5 = ANY (array{form.genero.data}) " \
                         f"OR g.genero_6 = ANY (array{form.genero.data}) " \
                         f"OR g.genero_7 = ANY (array{form.genero.data}) " \
                         f"OR g.genero_8 = ANY (array{form.genero.data}) " \
                         f"OR g.genero_9 = ANY (array{form.genero.data}) " \
                         f"OR g.genero_10 = ANY (array{form.genero.data}))"

        query = db.execute(f"SELECT * FROM mostrar_filmes_view v, genero g WHERE v.imdb_id=g.imdb_id"
                           f"{formAnoMin}{formAnoMax}{formDuracaoMin}{formDuracaoMax}{formNotaMin}"
                           f"{formNotaMax}{formGenero};").fetchall()

        if form.formaConsulta.data == 'Lista':

            return render_template('minhalista.html', query=query, form=form)

        if form.formaConsulta.data == 'Surpreenda-me':

            random_film = random.choice(query)
            query = [random_film]

            return render_template('minhalista.html', query=query, form=form)

    else:
        return render_template('minhalista.html', form=form)


@app.route("/filmes/<string:imdbID>", methods=['GET'])
def mostrar_detalhes_filme(imdbID):

    query = db.execute(f"SELECT * FROM mostrar_detalhes_filme_view WHERE imdb_id = '{imdbID}'").fetchall()

    existe_no_banco = db.execute(f"SELECT EXISTS (SELECT 1 FROM filme WHERE imdb_id='{imdbID}')").scalar()

    return render_template('detalhes.html', query=query, existe_no_banco=existe_no_banco)


if __name__ == "__main__":
    app.run(debug=True)