from wtforms import Form, BooleanField, StringField, PasswordField, validators
import email_validator
from wtforms.fields.html5 import EmailField
import sqlite3


class RegistrationForm(Form):
    name = StringField('NAME', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = EmailField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForms(Form):

    username = StringField('UserName', [validators.Length(min=6, max=35)])
    password = PasswordField(' Password', [validators.DataRequired()])
