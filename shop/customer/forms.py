from wtforms import Form, StringField, TextField, PasswordField, SelectField, validators, SubmitField, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from.models import Register


class CustomerRegistration(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = EmailField(
        'Email: ', [validators.email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm',
                                                                                          message='both password match must')])
    confirm = PasswordField('Repeate Password: ', [validators.DataRequired()])
    country = StringField('Country: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    state = StringField('State: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    address = StringField('Address:', [validators.DataRequired()])
    pincode = StringField('Pincode:', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(
        ['jpg', 'png', 'jpeg', 'gif'], 'image only')])

    submit = SubmitField('Register')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("This username already used")

    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This Email already used")


class CustomerLoginForm(FlaskForm):
    email = StringField(
        'Email: ', [validators.email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])
