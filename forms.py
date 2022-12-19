from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SelectField
from wtforms.validators import InputRequired, Length, Optional
from Genero import genero_options


class ConsultaForm(FlaskForm):

    formaConsulta = SelectField('Forma de consulta', choices=['Lista', 'Surpreenda-me'], validators=[InputRequired()])

    anoMin = StringField('Ano (mínimo)', validators=[Optional(), Length(min=4, max=4)])
    anoMax = StringField('Ano (máximo)', validators=[Optional(), Length(min=4, max=4)])

    duracaoMin = StringField('Duração em minutos (mínimo)', validators=[Optional(), Length(min=1, max=3)])
    duracaoMax = StringField('Duração em minutos (máximo)', validators=[Optional(), Length(min=1, max=3)])

    notaMin = StringField('Nota (mínimo)', validators=[Optional(), Length(min=1, max=3)])
    notaMax = StringField('Nota (máximo)', validators=[Optional(), Length(min=1, max=3)])

    genero = SelectMultipleField('Gênero(s)', choices=genero_options(), validators=[Optional()])
