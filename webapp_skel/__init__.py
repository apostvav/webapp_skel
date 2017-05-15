import os
#from logging import DEBUG
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#app.logger.setLevel(DEBUG)

# Database Configuration
app.config['SECRET_KEY'] = b'\xb66\x0cv\xe9P\xb4\xf8\xb8\xc6\xbc\xdb\xbaaaG\xb1e<>X"\x7f\x9b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'webapp_skel.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)

# Authentication Configuration
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

from .models import *
from .views import *
