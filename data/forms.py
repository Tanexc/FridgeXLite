from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField


class SearcherForm(FlaskForm):
    title = StringField(id="title")
    time = IntegerField(id="preparing_time")
    protein = IntegerField(id="protein")
    fats = IntegerField(id="fats")
    carboh = IntegerField(id="carboh")
    submit = SubmitField()
