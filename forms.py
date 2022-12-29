from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SelectField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Optional, NumberRange
from Genero import genero_options
import datetime


# Classe que define os fields do filtro da página "minhalista.html"
class ConsultaForm(FlaskForm):

    # Obter a data corrente
    today = datetime.date.today()

    # Field que retorna o forma de consulta, se em Lista ou Aleatório
    formaConsulta = SelectField('Forma de filtro:', choices=['Lista', 'Aleatório'], validators=[InputRequired()])

    # Fields que retornam a data inicial e data limite de parâmetro da pesquisa
    anoMin = IntegerField('Ano (mín):', validators=[Optional(), NumberRange(min=1900, max=today.year)])
    anoMax = IntegerField('Ano (máx):', validators=[Optional(), NumberRange(min=1900, max=today.year)])

    # Fields que rotrnam a duracao minima e a duracao maxima de parâmetro da pesquisa
    duracaoMin = IntegerField('Duração em minutos (mín):', validators=[Optional(), NumberRange(min=1, max=300)])
    duracaoMax = IntegerField('Duração em minutos (máx):', validators=[Optional(), NumberRange(min=1, max=300)])

    # Fields que retornam a nota minima e a nota maxiam de parâmetro da pesquisa
    notaMin = DecimalField('Nota (mín):', validators=[Optional(), NumberRange(min=0, max=10)])
    notaMax = DecimalField('Nota (máx):', validators=[Optional(), NumberRange(min=0, max=10)])

    # Field que retorna uma lista de gêneros requeridos pelo usuário como parâmetro
    genero = SelectMultipleField('Gênero(s):', choices=genero_options(), validators=[Optional()],
                                 render_kw={"data-placeholder": "Escolha..."})
