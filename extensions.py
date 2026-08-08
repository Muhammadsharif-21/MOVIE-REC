from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
api = Api()
bcrypt = Bcrypt()
Login_manager = LoginManager()