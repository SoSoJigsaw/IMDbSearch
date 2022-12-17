from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, FloatField
from wtforms.validators import InputRequired, Length, Optional


class ConsultaForm(FlaskForm):

    anoMin = IntegerField('Ano (mínimo)', validators=[Optional(), Length(min=4, max=4)])
    anoMax = IntegerField('Ano (máximo)', validators=[Optional(), Length(min=4, max=4)])

    duracaoMin = IntegerField('Duração em minutos (mínimo)', validators=[Optional(), Length(min=1, max=3)])
    duracaoMax = IntegerField('Duração em minutos (máximo)', validators=[Optional(), Length(min=1, max=3)])

    notaMin = FloatField('Nota (mínimo)', validators=[Optional(), Length(min=1, max=3)])
    notaMax = FloatField('Nota (máximo)', validators=[Optional(), Length(min=1, max=3)])

    genero = RadioField('Gênero(s)', choices=['Teste 1', 'Teste 2'], validators=[Optional()])