from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class PostForm(FlaskForm):
	title = TextAreaField('Event Title', validators=[
		DataRequired(), Length(min=1,max=140)])
	post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
	submit = SubmitField('Submit')
