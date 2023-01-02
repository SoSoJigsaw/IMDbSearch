import json
import random
import datetime
from sqlalchemy import create_engine
import requests
from flask import Flask, render_template, request, jsonify, flash, redirect, Markup
from forms import ConsultaForm

app = Flask(__name__)
app.secret_key = '1234'

# Conexão com o banco de dados
db = create_engine('postgresql://postgres:123@[localhost]/Filmes')


# Route que direciona à página inicial de pesquisa de filmes
@app.route("/")
def pesquisa():

    return render_template("index.html")


# Route que direciona à página de resultado, ou seja, do filme selecionada na pesquisa
@app.route("/resultado/<string:imdbID>", methods=['GET'])
def resultado(imdbID):

    # Consumo da OMDB API
    data_URL = f"http://www.omdbapi.com/?i={imdbID}&apikey=b0202a42"

    filme = requests.get(data_URL).json()

    # Reformatando os dados obtidos pela API para um formato que será aceito pelo banco de dados
    filme['Year'] = filme['Year'].replace('–', '')

    filme['Plot'] = filme['Plot'].replace("'", "`")
    filme['Title'] = filme['Title'].replace("'", "`")
    filme['Awards'] = filme['Awards'].replace("'", "`")
    filme['Actors'] = filme['Actors'].replace("'", "`")
    filme['Writer'] = filme['Writer'].replace("'", "`")

    # Reformatando ano, pra que apareça apenas a primeira data, no caso de séries que já terminaram
    filme['Year'] = filme['Year'][:4]

    # Caso o filme não tenha poster, setar "sem_imagem.gif" como a imagem source
    filme['Poster'] = filme['Poster'].replace('N/A', '/static/image/sem_imagem.gif')

    # Query de verificação se o filme consta no banco de dados, caso exista, o 'botão de remover' aparecerá,
    # caso não exista, o 'botão de adicionar é que aparecará'
    existe_no_banco = db.execute(f"SELECT EXISTS (SELECT 1 FROM filme WHERE imdb_id='{filme['imdbID']}')").scalar()

    return render_template('resultado.html', filme=filme, existe_no_banco=existe_no_banco)


# Route que direciona à tela de salvamento do filme no banco de dados. Depois de feito a rotina, caso realizada
# sem encontrar erros, ele redireciona à página da lista de filmes presentes no banco de daods
@app.route("/salvar/<string:imdbID>", methods=['GET'])
def salvar_filme(imdbID):

    # Consumindo a OMDB API
    data_URL = f"http://www.omdbapi.com/?i={imdbID}&apikey=b0202a42"

    filme = requests.get(data_URL).json()

    try:

        # Reformatando os dados obtidos pela API para um formato que será aceito pelo banco de dados
        filme['Year'] = filme['Year'].replace('–', '')

        filme['Runtime'] = filme['Runtime'].replace(' min', '')
        filme['Runtime'] = filme['Runtime'].replace('N/A', 'NULL')

        filme['imdbRating'] = filme['imdbRating'].replace('N/A', 'NULL')

        filme['Plot'] = filme['Plot'].replace("'", "`")
        filme['Title'] = filme['Title'].replace("'", "`")
        filme['Awards'] = filme['Awards'].replace("'", "`")
        filme['Actors'] = filme['Actors'].replace("'", "`")
        filme['Writer'] = filme['Writer'].replace("'", "`")

        # Reformatando ano, pra que apareça apenas a primeira data, no caso de séries que já terminaram
        filme['Year'] = filme['Year'][:4]

        filme['Poster'] = filme['Poster'].replace('N/A', '/static/image/sem_imagem.gif')

        # Query que faz o INSERT na tabela FILME do filme passado como parametro do route ( o imdbID) no banco de dados
        db.execute(f"INSERT INTO filme (imdb_id, titulo, ano, duracao_min, nota_imdb, sinopse, escrito_por, atores, "
                   f"idioma, pais, premios, poster) VALUES ('{filme['imdbID']}', '{filme['Title']}', {filme['Year']}, "
                   f"{filme['Runtime']}, {filme['imdbRating']}, '{filme['Plot']}', "
                   f"'{filme['Writer']}', '{filme['Actors']}', '{filme['Language']}', '{filme['Country']}', "
                   f"'{filme['Awards']}', '{filme['Poster']}')")

        print(f"'{filme['Title']}' adicionado à lista de filmes do usuário")

        # Looping que transforma o dado da API genero em uma lista python
        i = 0
        genre_string = filme['Genre']
        genre = []
        while i <= genre_string.count(','):
            if genre_string.count(',') == 0:
                genre.append(genre_string)
                i += 1
            else:
                genre.append(genre_string.split(",", genre_string.count(','))[i])
                i += 1

        # Tirando espaços desnecessarios presentes na lista genre
        i = 0
        while i <= len(genre) - 1:
            genre[i] = genre[i].replace(' ', '')
            i += 1

        # Query que faz o INSERT na tabela GENERO do filme passado como parametro do route ( o imdbID) no banco de dados
        db.execute(f"INSERT INTO genero VALUES ('{filme['imdbID']}', {str(genre)[1:-1]})")

        return redirect('/filmes')

    # Caso a rotina do route apresente algum erro ao salvar o filme no banco de dados, redirecionar à pagina de erro
    except:
        # Mensagem flash a ser monstrada no template
        flash(f"Não foi possível salvar '{filme['Title']}'. Verifique se o filme já consta em sua lista...")

        # Botao de retornar do template
        redirect_url = 'pesquisa'

        return render_template('error.html', url=redirect_url)


# Route que direciona a pagina de remover um filme do banco de dados, e caso a rotina ocorra sem nenhum erro,
# ele redicionara a pagina dos filmes listados no banco de dados
@app.route("/remover/<string:imdbID>", methods=['GET'])
def apagar_filme(imdbID):

    try:

        # Querys que excluem a linha referente ao filme passado como parametro na url (imdbID), nas tabelas
        # FILME e GENERO
        db.execute(f"DELETE FROM genero WHERE imdb_id= '{imdbID}';")

        db.execute(f"DELETE FROM filme WHERE imdb_id= '{imdbID}';")

        return redirect('/filmes')

    # Caso a rotina do route apresente algum erro ao remover o filme no banco de dados, redirecionar à pagina de erro
    except:

        # Mensagem flash a ser monstrada no template
        flash(f"Não foi possível remover o filme. Tente novamente...")

        # Botao de retornar no template
        redirect_url = 'mostrar_filmes'

        return render_template('error.html', url=redirect_url)


# Route que direciona a pagina de remover um filme do banco de dados, e caso a rotina ocorra sem nenhum erro,
# ele redicionara a pagina dos filmes listados no banco de dados
# No entanto, esse route também armazena os parâmetros de pesquisa, diferente do route anterior
@app.route("/remover/<string:imdbID>/<string:formaConsulta>/<int:anoMin>/<int:anoMax>/<int:duracaoMin>/"
           "<int:duracaoMax>/<string:notaMin>/<string:notaMax>/<string:genero>", methods=['GET'])
def apagar_filme_reload(imdbID, formaConsulta, anoMin, anoMax, duracaoMin, duracaoMax, notaMin, notaMax, genero):

    try:

        # Querys que excluem a linha referente ao filme passado como parametro na url (imdbID), nas tabelas
        # FILME e GENERO
        db.execute(f"DELETE FROM genero WHERE imdb_id= '{imdbID}';")

        db.execute(f"DELETE FROM filme WHERE imdb_id= '{imdbID}';")

        return redirect(f'/filmes/{formaConsulta}/{anoMin}/{anoMax}/{duracaoMin}/{duracaoMax}/{notaMin}/'
                        f'{notaMax}/{genero}')

    # Caso a rotina do route apresente algum erro ao remover o filme no banco de dados, redirecionar à pagina de erro
    except:

        # Mensagem flash a ser monstrada no template
        flash(f"Não foi possível remover o filme. Tente novamente...")

        # Botao de retornar no template
        redirect_url = 'mostrar_filmes'

        return render_template('error.html', url=redirect_url)


# Route que retorna a pagina onde é listado todos os filmes presentes no banco de dados junto com suas informações
@app.route("/filmes", methods=['GET'])
def mostrar_filmes():

    # Formulário do template
    form = ConsultaForm()

    # Query que retorna todas os filmes presentes no banco de dados a partir de uma view
    query = db.execute("SELECT * FROM mostrar_filmes_view;")

    # Caso a query retorne vazia, aparecer uma mensagem flash no template avisando que não há filmes na lista
    num_results = query.rowcount
    num_results = int(num_results)
    if num_results == 0:

        flash("Sua lista parece estar vazia. Que tal adicionar um filme?")

    return render_template('minhalista.html', query=query.fetchall(), form=form)


@app.route("/filmes", methods=['POST'])
def mostrar_filmes_post():

    # Formulário do template
    form = ConsultaForm()

    # Se o formulário for validado no envio, então prosseguir com o seguinte: se o valor do field for vazio ou nulo,
    # então setar o valor padrão reservado para o mesmo, nos casos da variável para o SQL e a variável para formatação
    # HTML. Caso não seja vazio ou nulo, então reservar em string para a variável SQL e reservar o valor do field para
    # a variável de formatação HTML.
    if form.validate_on_submit():
        if form.anoMin.data == '' or form.anoMin.data is None:
            formAnoMin = ''
            htmlAnoMin = 1900
        else:
            formAnoMin = f" AND v.ano >= {form.anoMin.data}"
            htmlAnoMin = form.anoMin.data

        if form.anoMax.data == '' or form.anoMax.data is None:
            formAnoMax = ''
            htmlAnoMax = datetime.date.today().year
        else:
            formAnoMax = f" AND v.ano <= {form.anoMax.data}"
            htmlAnoMax = form.anoMax.data

        if form.duracaoMin.data == '' or form.duracaoMin.data is None:
            formDuracaoMin = ''
            htmlDuracaoMin = 1
        else:
            formDuracaoMin = f" AND v.duracao_min >= {form.duracaoMin.data}"
            htmlDuracaoMin = form.duracaoMin.data

        if form.duracaoMax.data == '' or form.duracaoMax.data is None:
            formDuracaoMax = ''
            htmlDuracaoMax = 300
        else:
            formDuracaoMax = f" AND v.duracao_min <= {form.duracaoMax.data}"
            htmlDuracaoMax = form.duracaoMax.data

        if form.notaMin.data == '' or form.notaMin.data is None:
            formNotaMin = ''
            htmlNotaMin = 1
        else:
            formNotaMin = f" AND v.nota_imdb >= {form.notaMin.data}"
            htmlNotaMin = form.notaMin.data

        if form.notaMax.data == '' or form.notaMax.data is None:
            formNotaMax = ''
            htmlNotaMax = 10
        else:
            formNotaMax = f" AND v.nota_imdb <= {form.notaMax.data}"
            htmlNotaMax = form.notaMax.data

        if not form.genero.data:
            formGenero = ''
            htmlGenero = 'Todos'
            urlGenero = 'Todos'
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

            # Retirando '[' e ']', e convertendo a lista field genero em uma string única
            htmlGenero = str(form.genero.data)[1:-1]
            htmlGenero = htmlGenero.replace("'", "")

            # Colocando asterístico no lugar da vírgula para gerar um url válido
            urlGenero = htmlGenero.replace(", ", "*")

        formaConsulta = form.formaConsulta.data

        # Query que retorna todos os filmes correspondentes no banco de dados com os parâmetros fornecidos nos fields
        # na clásula WHERE
        query = db.execute(f"SELECT * FROM mostrar_filmes_view v, genero g WHERE v.imdb_id=g.imdb_id"
                           f"{formAnoMin}{formAnoMax}{formDuracaoMin}{formDuracaoMax}{formNotaMin}"
                           f"{formNotaMax}{formGenero} ORDER BY v.datahora DESC;")

        # Variável de marcação de texto para ser apresentado no template, que retorna todos os valores dos parâmetros
        # fornecidos pelo usuário no formulário
        parametros = Markup(f'<h1 class="parametros-pesquisa"> '
                            f'<b>Modo:</b> {formaConsulta}, '
                            f'<b>Ano:</b> de {htmlAnoMin} até {htmlAnoMax}, '
                            f'<b>Duração:</b> de {htmlDuracaoMin} até {htmlDuracaoMax} minutos, '
                            f'<b>Nota:</b> de {htmlNotaMin} até {htmlNotaMax}, '
                            f'<b>Gênero(s):</b> {htmlGenero}.</h1>')

        # Botão de resetar a pesquisa, redirecionando ao método GET da página
        botao_resetar = ''

        # Caso a query retorne vazia, aparecer uma mensagem flash no template avisando que não há filmes na lista
        num_results = query.rowcount
        num_results = int(num_results)
        if num_results == 0:
            flash("Nenhum filme corresponde aos parâmetros fornecidos...")

            return render_template('minhalista.html', form=form, parametros=parametros, resetar=botao_resetar)

        # Caso contrário, ou seja, caso a query não retorne vazia...
        else:

            # Caso o valor entregue pelo usuário no field do formulário 'forma de consulta' seja 'Lista'
            if formaConsulta == 'Lista':

                return render_template('minhalista.html', query=query.fetchall(), form=form, parametros=parametros,
                                       html=[formaConsulta, htmlAnoMin, htmlAnoMax, htmlDuracaoMin, htmlDuracaoMax, htmlNotaMin,
                                             htmlNotaMax, urlGenero], resetar=botao_resetar)

            # Caso o valor entregue pelo usuário no field do formulário 'forma de consulta' seja 'Aleatório'
            if formaConsulta == 'Aleatório':

                # Utilizando a biblioteca random para randomizar a escolha de um filme dentre os disponíveis na query
                query = query.fetchall()
                random_film = random.choice(query)
                query = [random_film]

                return render_template('minhalista.html', query=query, form=form, parametros=parametros,
                                       html=[formaConsulta, htmlAnoMin, htmlAnoMax, htmlDuracaoMin, htmlDuracaoMax, htmlNotaMin,
                                             htmlNotaMax, urlGenero], resetar=botao_resetar)

    # Caso o formulário não seja validado durante o envio, gerar uma mensagem flash e renderizar à página de erro
    else:

        flash("Os parâmetros fornecidos não são válidos. Tente novamente...")

        redirect_url = 'mostrar_filmes'

        return render_template('error.html', url=redirect_url)


# Route que redireciona à página onde fornece todos os filmes presentes no banco de dados, no entanto mantendo os
# parâmetros da última pesquisa enviada através do formulário.
# Esse route é utilizado para retornar à página da lista de filmes após ter saído dela, mantendo todos os parâmetros
# da última pesquisa realizada, facilitando assim a usabilidade do usuário
@app.route("/filmes/<string:formaConsulta>/<int:anoMin>/<int:anoMax>/<int:duracaoMin>/<int:duracaoMax>/<string:notaMin"
           ">/<string:notaMax>/<string:genero>", methods=['GET'])
def mostrar_filmes_reload(formaConsulta, anoMin, anoMax, duracaoMin, duracaoMax, notaMin, notaMax, genero):

    # Formulário do template
    form = ConsultaForm()

    # Gerando as variáveis de comando SQL e de formatação HTML, a partir dos valores das variáveis da url do route
    formAnoMin = f" AND v.ano >= {anoMin}"
    htmlAnoMin = anoMin

    formAnoMax = f" AND v.ano <= {anoMax}"
    htmlAnoMax = anoMax

    formDuracaoMin = f" AND v.duracao_min >= {duracaoMin}"
    htmlDuracaoMin = duracaoMin

    formDuracaoMax = f" AND v.duracao_min <= {duracaoMax}"
    htmlDuracaoMax = duracaoMax

    formNotaMin = f" AND v.nota_imdb >= {notaMin}"
    htmlNotaMin = notaMin

    formNotaMax = f" AND v.nota_imdb <= {notaMax}"
    htmlNotaMax = notaMax

    if genero == 'Todos':
        formGenero = ''
        htmlGenero = 'Todos'
        urlGenero = 'Todos'

    else:
        genero = genero.replace("*", ", ")
        genero = genero.split(', ')

        formGenero = f" AND (g.genero_1 = ANY (array{genero}) " \
                     f"OR g.genero_2 = ANY (array{genero}) " \
                     f"OR g.genero_3 = ANY (array{genero}) " \
                     f"OR g.genero_4 = ANY (array{genero}) " \
                     f"OR g.genero_5 = ANY (array{genero}) " \
                     f"OR g.genero_6 = ANY (array{genero}) " \
                     f"OR g.genero_7 = ANY (array{genero}) " \
                     f"OR g.genero_8 = ANY (array{genero}) " \
                     f"OR g.genero_9 = ANY (array{genero}) " \
                     f"OR g.genero_10 = ANY (array{genero}))"

        # Retirando '[' e ']', e convertendo a lista field genero em uma string única
        htmlGenero = str(genero)[1:-1]
        htmlGenero = htmlGenero.replace("'", "")

        # Colocando asterístico no lugar da vírgula para gerar um url válido
        urlGenero = htmlGenero.replace(", ", "*")

    # Query que retorna todos os filmes correspondentes no banco de dados com os parâmetros fornecidos nos fields
    # na clásula WHERE
    query = db.execute(f"SELECT * FROM mostrar_filmes_view v, genero g WHERE v.imdb_id=g.imdb_id"
                       f"{formAnoMin}{formAnoMax}{formDuracaoMin}{formDuracaoMax}{formNotaMin}"
                       f"{formNotaMax}{formGenero} ORDER BY v.datahora DESC;")

    # Variável de marcação de texto para ser apresentado no template, que retorna todos os valores dos parâmetros
    # fornecidos pelo usuário no formulário
    parametros = Markup(f'<h1 class="parametros-pesquisa"> '
                        f'<b>Modo:</b> {formaConsulta}, '
                        f'<b>Ano:</b> de {htmlAnoMin} até {htmlAnoMax}, '
                        f'<b>Duração:</b> de {htmlDuracaoMin} até {htmlDuracaoMax} minutos, '
                        f'<b>Nota:</b> de {htmlNotaMin} até {htmlNotaMax}, '
                        f'<b>Gênero(s):</b> {htmlGenero}.</h1>')

    # Botão de resetar a pesquisa, redireciona ao método GET da página
    botao_resetar = ''

    # Caso o valor entregue pela variável do url do route em 'formaConsulta' seja 'Lista'
    if formaConsulta == 'Lista':
        return render_template('minhalista.html', query=query.fetchall(), form=form, parametros=parametros,
                               html=[formaConsulta, htmlAnoMin, htmlAnoMax, htmlDuracaoMin, htmlDuracaoMax, htmlNotaMin,
                                     htmlNotaMax, urlGenero], resetar=botao_resetar)

    # Caso o valor entregue pela variável do url do route em 'formaConsulta' seja 'Aleatório'
    if formaConsulta == 'Aleatório':
        query = query.fetchall()
        random_film = random.choice(query)
        query = [random_film]

        return render_template('minhalista.html', query=query, form=form, parametros=parametros,
                               html=[formaConsulta, htmlAnoMin, htmlAnoMax, htmlDuracaoMin, htmlDuracaoMax, htmlNotaMin,
                                     htmlNotaMax, urlGenero], resetar=botao_resetar)


# Route que direciona à página onde mostra mais detalhes sobre o filme, ao selecioná-lo na tabela de filmes presentes
# no banco de dados
@app.route("/filmes/<string:imdbID>", methods=['GET'])
def mostrar_detalhes_filme(imdbID):

    # Query que retorna todos os dados referentes ao filme passado como parâmetro na variável de url (imdbID)
    query = db.execute(f"SELECT * FROM mostrar_detalhes_filme_view WHERE imdb_id = '{imdbID}'").fetchall()

    # Query de verificação se o filme consta no banco de dados, caso exista, o 'botão de remover' aparecerá,
    # caso não exista, o 'botão de adicionar é que aparecará'
    existe_no_banco = db.execute(f"SELECT EXISTS (SELECT 1 FROM filme WHERE imdb_id='{imdbID}')").scalar()

    return render_template('detalhes.html', query=query, existe_no_banco=existe_no_banco)


# Route que direciona à página onde mostra mais detalhes sobre o filme, ao selecioná-lo na tabela de filmes presentes
# no banco de dados
# No entanto, o que difere este do route anterior, é que este é acionado quando é passado os parâmetros da pesquisa
# do usuário através da url.
# Este route é utilizado para armazenar os parâmetros de pesquisa do usuário mesmo após sair da página de filtragem
@app.route("/filmes/<string:imdbID>/<string:formaConsulta>/<int:anoMin>/<int:anoMax>/<int:duracaoMin>/<int:duracaoMax"
           ">/<string:notaMin>/<string:notaMax>/<string:genero>", methods=['GET'])
def mostrar_detalhes_filme_reload(imdbID, formaConsulta, anoMin, anoMax, duracaoMin, duracaoMax, notaMin,
                                      notaMax, genero):

    # Query que retorna todos os dados referentes ao filme passado como parâmetro na variável de url (imdbID)
    query = db.execute(f"SELECT * FROM mostrar_detalhes_filme_view WHERE imdb_id = '{imdbID}'").fetchall()

    # Query de verificação se o filme consta no banco de dados, caso exista, o 'botão de remover' aparecerá,
    # caso não exista, o 'botão de adicionar é que aparecará'
    existe_no_banco = db.execute(f"SELECT EXISTS (SELECT 1 FROM filme WHERE imdb_id='{imdbID}')").scalar()

    return render_template('detalhes.html', query=query, existe_no_banco=existe_no_banco,
                           html=[formaConsulta, anoMin, anoMax, duracaoMin, duracaoMax, notaMin, notaMax, genero])


if __name__ == "__main__":
    app.run(debug=True)
