from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config.from_object("config.AppConfig")

db = SQLAlchemy(app)
migrate = Migrate(app,db)
ma = Marshmallow(app)
jwt = JWTManager(app)

CORS(app)

from api import blueprint

app.register_blueprint(blueprint)