from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, EqualTo, Email
from wtforms.fields.html5 import EmailField


class SignUp(FlaskForm):
  username = StringField('username', validators=[InputRequired()])
  email = EmailField('email', validators=[Email(), InputRequired()])
  password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
  confirm  = PasswordField('Repeat Password')
  submit = SubmitField('Sign Up', render_kw={'class': 'btn waves-effect waves-light white-text'})

class LogIn(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn waves-effect waves-light white-text'})
  

class AddIngredient(FlaskForm):
  name = TextAreaField('Ingredient', validators =[InputRequired()])
  submit = SubmitField('Add', render_kw={'class': 'btn waves-effect waves-light white-text'})
  