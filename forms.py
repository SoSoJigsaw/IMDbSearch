from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SelectField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Optional, NumberRange
from Genero import genero_options
import datetime


class ConsultaForm(FlaskForm):

    today = datetime.date.today()

    formaConsulta = SelectField('Forma de filtro:', choices=['Lista', 'Aleatório'], validators=[InputRequired()])

    anoMin = IntegerField('Ano (mín):', validators=[Optional(), NumberRange(min=1900, max=today.year)])
    anoMax = IntegerField('Ano (máx):', validators=[Optional(), NumberRange(min=1900, max=today.year)])

    duracaoMin = IntegerField('Duração em minutos (mín):', validators=[Optional(), NumberRange(min=1, max=300)])
    duracaoMax = IntegerField('Duração em minutos (máx):', validators=[Optional(), NumberRange(min=1, max=300)])

    notaMin = DecimalField('Nota (mín):', validators=[Optional(), NumberRange(min=0, max=10)])
    notaMax = DecimalField('Nota (máx):', validators=[Optional(), NumberRange(min=0, max=10)])

    genero = SelectMultipleField('Gênero(s):', choices=genero_options(), validators=[Optional()],
                                 render_kw={"data-placeholder": "Escolha..."})
