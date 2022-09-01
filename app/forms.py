from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, Form, SelectField 
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """Forms used for login page"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    #remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class searchFormExampleUsers(FlaskForm):
      """Example Search form, will be removed/edited later.
      Right now searches/queries users table. Later will be chnaged to search 
      our actual db tables when they are finalised. 
      Searches by Username or id"""
      search_choices = [('id', 'id')]
      select = SelectField('Search for user:', search_choices=search_choices)
      search = StringField('')
      submit = SubmitField('Search')

