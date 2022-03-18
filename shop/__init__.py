from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .admin import forms
import os
from flask_msearch import Search
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
app_root = app.config['UPLOAD_FOLDER'] = "static/images/"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['SECRET_KEY'] = 'peraman123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"Please login first"


from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customer import routes

