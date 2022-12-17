from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, FloatField
from wtforms.validators import InputRequired, Length, Optional


class ConsultaForm(FlaskForm):

    anoMin = StringField('Ano (mínimo)', validators=[Optional(), Length(min=4, max=4)])
    anoMax = StringField('Ano (máximo)', validators=[Optional(), Length(min=4, max=4)])

    duracaoMin = StringField('Duração em minutos (mínimo)', validators=[Optional(), Length(min=1, max=3)])
    duracaoMax = StringField('Duração em minutos (máximo)', validators=[Optional(), Length(min=1, max=3)])

    notaMin = StringField('Nota (mínimo)', validators=[Optional(), Length(min=1, max=3)])
    notaMax = StringField('Nota (máximo)', validators=[Optional(), Length(min=1, max=3)])

    genero = RadioField('Gênero(s)', choices=['Teste 1', 'Teste 2'], validators=[Optional()])