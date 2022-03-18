from flask_wtf.file import FileAllowed, FileField, FileRequired, FileStorage
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField, FloatField


class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    colors = TextAreaField('colors', [validators.DataRequired()])

    image1 = FileField('image1', validators=[
                       FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image2 = FileField('image2', validators=[
                       FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image3 = FileField('image3', validators=[
                       FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
